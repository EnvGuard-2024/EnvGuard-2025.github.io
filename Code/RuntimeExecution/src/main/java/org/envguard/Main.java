package org.envguard;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.envguard.environment.device.*;
import org.envguard.environment.state.*;
import org.envguard.WebSocket.WebSocketClient;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import javax.websocket.DeploymentException;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import java.io.IOException;

public class Main {
    public static List<List<Object>> err_action = new ArrayList<>();
    public static Map<String, Object> ltl_table = new HashMap<>();
    public static final List<String> device_list = new ArrayList<>();
    public static final List<String> state_list = new ArrayList<>();
    static WebSocketClient client;
    public static List<Map<String, Object>> dataList;

    public static void main(String[] args) throws DeploymentException, URISyntaxException, IOException {
        init();
        getDir("./environment/device", "device");
        getDir("./environment/state", "state");
        receiveMessage();
    }
    private static void init(){
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            dataList = objectMapper.readValue(
                    new File("./RuntimeExecution/src/main/resources/MTLProperty.json"),
                    new TypeReference<>() {
                    }
            );
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    private static void getDir(String dir, String type) {
        traverseDirectory(dir, type);
    }

    private static void traverseDirectory(String dirPath, String type) {
        File directory = new File(dirPath);
        if (directory.exists() && directory.isDirectory()) {
            File[] files = directory.listFiles();
            if (files != null) {
                for (File file : files) {
                    if (file.isFile()) {
                        if (type == "device") device_list.add(file.getName());
                        else state_list.add(file.getName());
                    } else if (file.isDirectory() && (file.getName().equals("device") || file.getName().equals("state"))) {
                        traverseDirectory(file.getAbsolutePath(), type);
                    }
                }
            }
        }
    }

    private static List<String[]> change(String string) {
        List<String[]> stringList = new ArrayList<>();
        Pattern pattern = Pattern.compile("[a-zA-Z.!]+");
        Matcher matcher = pattern.matcher(string);

        while (matcher.find()) {
            String value = matcher.group();
            if (value.split("\\.").length == 2) {
                return null;
            }

            String tempValue = value;
            String symbol = "==";

            if (value.contains("!")) {
                symbol = "!=";
                tempValue = value.substring(1);
            }
            String[] tempList = tempValue.split("\\.");

            if (device_list.contains(tempList[1])) {
                String end;

                if (tempList[2].equals("on")) {
                    end = "1";
                } else {
                    end = "0";
                }

                String temp = "env.get(\"space_dict\").get(\"" + tempList[0] + "\").get(\"device_dict\").get(\"" + tempList[1] + "\").get() " + symbol + " " + end;
                stringList.add(new String[]{value, temp});
            } else {
                String end;

                if (!tempList[1].equals("HumanState") && !tempList[1].equals("Weather")) {
                    if (tempList[2].equals("low")) {
                        end = "-1";
                    } else if (tempList[2].equals("middle")) {
                        end = "0";
                    } else {
                        end = "1";
                    }
                } else if (tempList[1].equals("HumanState")) {
                    if (tempList[2].equals("detected")) {
                        end = "1";
                    } else {
                        end = "0";
                    }
                } else {
                    end = "'" + tempList[2] + "'";
                }
                String temp = "env.get(\"space_dict\").get(\"" + tempList[0] + "\").get(\"env_state\").get(\"" + tempList[1] + "\").get() " + symbol + " " + end;
                stringList.add(new String[]{value, temp});
            }
        }
        return stringList;
    }

    private static List<String> getAction(Map<String, Map<String, Map<String, Map<String, Object>>>> env, String condition) {
        List<String> result = new ArrayList<>();

        ObjectMapper objectMapper = new ObjectMapper();
        Map<String, Map<String, Map<String, Integer>>> map = null;
        try {
            map = objectMapper.readValue(condition, Map.class);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        for (Map.Entry<String, Map<String, Map<String, Integer>>> roomEntry : map.entrySet()) {
            String room = roomEntry.getKey();

            Map<String, Object> devices = env.get("space_dict").get(room).get("device_dict");
            for (Map.Entry<String, Object> deviceEntry : devices.entrySet()) {
                String device = deviceEntry.getKey();
                int deviceValue = (int) deviceEntry.getValue();
                int conValue = (int) map.get(room).get("device_dict").get(device);

                if (deviceValue > conValue) {
                    result.add(device + "_off");
                } else if (deviceValue < conValue) {
                    result.add(device + "_on");
                }
            }

            Map<String, Object> states = env.get("space_dict").get(room).get("env_state");
            for (Map.Entry<String, Object> stateEntry : states.entrySet()) {
                String state = stateEntry.getKey();
                int stateValue = (int) stateEntry.getValue();
                int conValue = (int) map.get(room).get("env_state").get(state);

                if (stateValue > conValue) {
                    result.add(state + "_down");
                } else if (stateValue < conValue) {
                    result.add(state + "_up");
                }
            }
        }

        return result;
    }

    private static Object sendURL(String urlString, String type) {
        try {
            URL url = new URL(urlString);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod(type);

            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            StringBuilder response = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }

            reader.close();

            System.out.println("Response Content:");
            System.out.println(response.toString());

            connection.disconnect();
            return response;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void check(Map<String, Object> regulation, long times) throws ScriptException, IOException {
        List<String> mtl_err_action = null;
        while (System.currentTimeMillis() <= times) {
            Map<String, String> receivedMessage = null;
            for (String pair : client.message.split(";")) {
                String[] keyValue = pair.split("=", 2);
                if (keyValue.length == 2) {
                    String key = keyValue[0].trim();
                    String value = keyValue[1].trim();
                    receivedMessage.put(key, value);
                }
            }
            String urlString;
            if (receivedMessage.get("type").equals("device")) {
                urlString = "http://10.177.29.226:5002/set_device_value/" + receivedMessage.get("room") + "/" + receivedMessage.get("device") + "/" + receivedMessage.get("value");
            } else {
                urlString = "http://10.177.29.226:5002/set_state_value/" + receivedMessage.get("room") + "/" + receivedMessage.get("state") + "/" + receivedMessage.get("value");
            }
            sendURL(urlString, "POST");

            Map<String, Map<String, Map<String, Map<String, Object>>>> env = getEnvironment();
            mtl_err_action = getAction(env, (String) regulation.get("condition"));
            err_action.get(1).add(mtl_err_action);
            if (regulation.get("flag").equals("F")) {
                try {
                    ScriptEngineManager manager = new ScriptEngineManager();
                    ScriptEngine engine = manager.getEngineByName("js");
                    Object result = engine.eval((String) regulation.get("condition"));
                    if (result instanceof Boolean && ((Boolean) result)) {
                        List<String> fix_list = new ArrayList<>();
                        if (regulation.get("contact").equals("or")) {
                            List<String> temp = Arrays.asList(((String)regulation.get("fix")).split(","));
                            for (String fix : temp) {
                                String f = Arrays.asList(fix.split(",")).get(1);
                                if (!f.isEmpty() && engine.eval(f) instanceof Boolean)
                                    fix_list.add(Arrays.asList(fix.split(",")).get(0));
                                else if (f.isEmpty()) fix_list.add(Arrays.asList(fix.split(",")).get(0));
                            }
                        }
                        client.sendMessage(reCheck(fix_list).toString());
                        return;
                    }
                } catch (ScriptException e) {
                    e.printStackTrace();
                }
            } else {
                try {
                    ScriptEngineManager manager = new ScriptEngineManager();
                    ScriptEngine engine = manager.getEngineByName("js");
                    Object result = engine.eval((String) regulation.get("condition"));
                    if (result instanceof Boolean && !((Boolean) result)) {
                        return;
                    }
                } catch (ScriptException e) {
                    e.printStackTrace();
                }
            }
        }

        if (regulation.get("contact").equals("or")) {
            ScriptEngineManager manager = new ScriptEngineManager();
            ScriptEngine engine = manager.getEngineByName("js");
            Object result = engine.eval((String) regulation.get("condition"));
            if (result instanceof Boolean && ((Boolean) result)) {
                List<String> fix_list = new ArrayList<>();
                String[] temp = ((String)regulation.get("fix")).split(",");
                for (String fix : temp) {
                    String f = Arrays.asList(fix.split(",")).get(1);
                    if (!f.isEmpty() && engine.eval(f) instanceof Boolean)
                        fix_list.add(Arrays.asList(fix.split(",")).get(0));
                    else if (f.isEmpty()) fix_list.add(Arrays.asList(fix.split(",")).get(0));
                }
                client.sendMessage(reCheck(fix_list).toString());
                return;
            }
        }
        err_action.get(1).remove(mtl_err_action);
    }

    private static Map<String, Object> getDict(String spaceName, Map<String, Map<String, Object>> space) {
        Map<String, Object> temp = new HashMap<>();
        temp.put("action_dict", new HashMap<String, Object>());
        temp.put("enable_dict", new HashMap<String, Object>());
        temp.put("ext_action_list", new ArrayList<String>());

        Map<String, Object> deviceDict = space.get("device_dict");
        for (Map.Entry<String, Object> device : deviceDict.entrySet()) {
            String key = device.getKey();
            Map<String, Map<String, String>> value = (Map<String, Map<String, String>>) device.getValue();

            Map<String, String> actionDict = value.get("action_dict");
            for (Map.Entry<String, String> actionEntry : actionDict.entrySet()) {
                String actionKey = actionEntry.getKey();
                Object actionValue = actionEntry.getValue();
                String name = spaceName + "." + key + "." + actionKey;
                ((Map<String, Object>) temp.get("action_dict")).put(name, actionValue);
            }

            Map<String, String> enableDict = value.get("enable_dict");
            for (Map.Entry<String, String> enableEntry : enableDict.entrySet()) {
                String enableKey = enableEntry.getKey();
                Object enableValue = enableEntry.getValue();
                String name = spaceName + "." + key + "." + enableKey;
                ((Map<String, Object>) temp.get("enable_dict")).put(name, enableValue);
            }
            List<String> extActionList = new ArrayList<>(value.get("ext_action_list").values());
            for (String item : extActionList) {
                ((List<String>) temp.get("ext_action_list")).add(spaceName + "." + key + "." + item);
            }
        }

        Map<String, Object> stateDict;
        stateDict = space.get("env_state");
        for (Map.Entry<String, Object> device : stateDict.entrySet()) {
            String key = device.getKey();
            Map<String, Map<String, String>> value = (Map<String, Map<String, String>>) device.getValue();

            Map<String, String> actionDict = value.get("action_dict");
            for (Map.Entry<String, String> actionEntry : actionDict.entrySet()) {
                String actionKey = actionEntry.getKey();
                Object actionValue = actionEntry.getValue();
                String name = spaceName + "." + key + "." + actionKey;
                ((Map<String, Object>) temp.get("action_dict")).put(name, actionValue);
            }

            Map<String, String> enableDict = value.get("enable_dict");
            for (Map.Entry<String, String> enableEntry : enableDict.entrySet()) {
                String enableKey = enableEntry.getKey();
                Object enableValue = enableEntry.getValue();
                String name = spaceName + "." + key + "." + enableKey;
                ((Map<String, Object>) temp.get("enable_dict")).put(name, enableValue);
            }
            List<String> extActionList = new ArrayList<>(value.get("ext_action_list").values());
            for (String item : extActionList) {
                ((List<String>) temp.get("ext_action_list")).add(spaceName + "." + key + "." + item);
            }
        }

        return temp;
    }

    public static Map<String, Map<String, Map<String, Map<String, Object>>>> getEnvironment() {
        Map<String, Map<String, Map<String, Map<String, Object>>>> env = new HashMap<>();
        Map<String, Map<String, Map<String, Object>>> spaceDict = new HashMap<>();

        String urlString = "http://10.177.29.226:5002/room_list";
        String[] roomList = (String[]) sendURL(urlString, "GET");
        for (String room : roomList) {
            Map<String, Object> deviceDict = new HashMap<>();
            Map<String, Object> envState = new HashMap<>();

            urlString = "http://10.177.29.226:5002/room_state/" + room;
            String[] roomState = (String[]) sendURL(urlString, "GET");
            Object temperature = null;
            Object brightness = null;
            Object airquality = null;
            Object humanstate = null;
            Object humidity = null;
            Object noise = null;
            Object weather = null;

            for (String state : roomState) {
                switch (state) {
                    case "Temperature":
                        temperature = new Temperature();
                        envState.put("Temperature", temperature);
                        break;
                    case "Brightness":
                        brightness = new Brightness();
                        envState.put("Brightness", brightness);
                        break;
                    case "AirQuality":
                        airquality = new AirQuality();
                        envState.put("AirQuality", airquality);
                        break;
                    case "HumanState":
                        humanstate = new HumanState();
                        envState.put("HumanState", humanstate);
                        break;
                    case "Humidity":
                        humidity = new Humidity();
                        envState.put("Humidity", humidity);
                        break;
                    case "Noise":
                        noise = new Noise();
                        envState.put("Noise", noise);
                        break;
                    case "Weather":
                        weather = new Weather();
                        envState.put("Weather", weather);
                        break;
                }
            }

            urlString = "http://10.177.29.226:5002/room_device/" + room;
            String[] roomDevice = (String[]) sendURL(urlString, "GET");

            for (String device : roomDevice) {
                switch (device.substring(0, device.length() - 3)) {
                    case "AC":
                        deviceDict.put("AC", new AC());
                        break;
                    case "Window":
                        deviceDict.put("Window", new Window());
                        break;
                    case "Light":
                        deviceDict.put("Light", new Light());
                        break;
                    case "Curtain":
                        deviceDict.put("Curtain", new Curtain());
                        break;
                    case "Door":
                        deviceDict.put("Door", new Door());
                        break;
                    case "Heater":
                        deviceDict.put("Heater", new Heater());
                        break;
                    case "Humidifier":
                        deviceDict.put("Humidifier", new Humidifier());
                        break;
                    case "MicrowaveOven":
                        deviceDict.put("MicrowaveOven", new MicrowaveOven());
                        break;
                    case "Printer":
                        deviceDict.put("Printer", new Printer());
                        break;
                    case "AirPurifier":
                        deviceDict.put("AirPurifier", new AirPurifier());
                        break;
                    case "Speaker":
                        deviceDict.put("Speaker", new Speaker());
                        break;
                    case "TV":
                        deviceDict.put("TV", new TV());
                        break;
                    case "WaterDispenser":
                        deviceDict.put("WaterDispenser", new WaterDispenser());
                        break;
                }
            }

            Map<String, Map<String, Object>> roomTemp = new HashMap<>();
            roomTemp.put("device_dict", deviceDict);
            roomTemp.put("env_state", envState);
            Map<String, Object> temp = getDict(room, roomTemp);
            roomTemp.put("action_dict", (Map<String, Object>) temp.get("action_dict"));
            roomTemp.put("enable_dict", (Map<String, Object>) temp.get("enable_dict"));
            roomTemp.put("ext_action_list", (Map<String, Object>) temp.get("ext_action_list"));
            spaceDict.put(room, roomTemp);
        }

        env.put("space_dict", spaceDict);
        return env;
    }

    public static void receiveMessage() throws DeploymentException, URISyntaxException, IOException {
        String file = "./OfflineAnalysis/LTL/result/state_action.xlsx";
        try (FileInputStream fis = new FileInputStream(file);
             Workbook workbook = new XSSFWorkbook(fis)) {

            Sheet sheet = workbook.getSheetAt(0);
            int rowIndex = 0;
            for (Row row : sheet) {
                if (rowIndex == 0) {
                    rowIndex++;
                    continue;
                }
                Cell stateCell = row.getCell(0);
                Cell actionCell = row.getCell(1);
                Cell fixCell = row.getCell(2);

                String state = "";
                String action = "";
                String fix = "";

                if (stateCell != null && stateCell.getCellType() == CellType.STRING) {
                    state = stateCell.getStringCellValue();
                }

                if (actionCell != null && actionCell.getCellType() == CellType.STRING) {
                    action = actionCell.getStringCellValue();
                }

                if (fixCell != null && fixCell.getCellType() == CellType.STRING) {
                    fix = fixCell.getStringCellValue();
                }

                Map<String, Object> temp = new HashMap<>();
                temp.put("action", change(action));
                temp.put("fix", fix);
                ltl_table.put(state, temp);
                rowIndex++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        String url = "ws://event/websocket";
        client = new WebSocketClient();
        client.connect(url);
    }

    public static List<String> reCheck(List<String> fixList) {
        List<String> result = new ArrayList<>();
        for (int i = 0; i < fixList.size(); i++) {
            String fix = fixList.get(i);
            if (err_action.get(0).contains(fix)) {
                continue;
            }
            boolean found = false;
            for (Object mtlErr : err_action.get(1)) {
                if (((String) mtlErr).contains(fix)) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                result.add(fix);
            }
        }
        return result;
    }
}
