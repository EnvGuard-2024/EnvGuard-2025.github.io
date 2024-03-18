package org.envguard.WebSocket;

import org.json.JSONObject;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import javax.websocket.*;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import static org.envguard.Main.*;

@ClientEndpoint
public class WebSocketClient {
    private Session session;
    public String message;

    @OnOpen
    public void onOpen(Session session) {
        this.session = session;
        System.out.println("Connected to server");
    }

    @OnMessage
    public void onMessage(String mess) {
        message = mess;
        try {
            JSONObject jsonMessage = new JSONObject(mess);
            if (jsonMessage.getString("type").equals("device")) {
                String url = "http://10.177.29.226:5002/set_device_value/" +
                        jsonMessage.getString("room") + "/" +
                        jsonMessage.getString("device") + "/" +
                        jsonMessage.getString("value");
                sendHttpGetRequest(url);
            } else {
                String url = "http://10.177.29.226:5002/set_state_value/" +
                        jsonMessage.getString("room") + "/" +
                        jsonMessage.getString("state") + "/" +
                        jsonMessage.getString("value");
                sendHttpGetRequest(url);
            }
            String env = getEnvironment().toString();
            Object temp_action = ((Map<String, Object>) ltl_table.get(env)).get("action");
            List<Object> convertedList = new ArrayList<>();
            convertedList.add(temp_action);
            err_action.set(0, convertedList);
            for (Map<String, Object> regulation : dataList) {
                ScriptEngineManager manager = new ScriptEngineManager();
                ScriptEngine engine = manager.getEngineByName("js");
                Object result = engine.eval((String) regulation.get("trigger"));
                if (result instanceof Boolean && ((Boolean) result)) {
                    Thread receiveThread = new Thread(() -> {
                        try {
                            check(regulation, System.currentTimeMillis() + 60 * Integer.parseInt((String) regulation.get("time")));
                        } catch (ScriptException e) {
                            throw new RuntimeException(e);
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    });
                    receiveThread.start();
                }
            }
            temp_action = ((Map<String, Object>) ltl_table.get(env)).get("action");
            convertedList.clear();
            convertedList.add(temp_action);
            if (convertedList.contains(mess)) {
                sendMessage(reCheck((List<String>) ((Map<?, ?>) ltl_table.get(env)).get("fix")).toString());
            }
        } catch (ScriptException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @OnClose
    public void onClose(CloseReason reason) {
        System.out.println("Connection closed: " + reason);
    }

    @OnError
    public void onError(Throwable throwable) {
        System.out.println("Error occurred: " + throwable.getMessage());
    }

    public void connect(String serverUri) throws URISyntaxException, IOException, DeploymentException {
        WebSocketContainer container = ContainerProvider.getWebSocketContainer();
        try {
            container.connectToServer(WebSocketClient.class, new URI(serverUri));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void sendMessage(String message) throws IOException {
        session.getBasicRemote().sendText(message);
    }

    public static void sendHttpGetRequest(String url) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .build();

        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            String responseBody = response.body();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void close() throws IOException {
        session.close();
    }
}
