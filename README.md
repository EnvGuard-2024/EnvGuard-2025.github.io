# EnvGuard-2024.github.io


## Dataset
We collected data in each of the two real-world WoT environments and built a dataset to evaluate EnvGuard. The dataset is publicly available.   
The dataset for the office environment is as follows:
([Office Dataset](https://github.com/EnvGuard-2024/EnvGuard-2024.github.io/tree/master/DataSet/OfficeEnvironment))  
The dataset for the home environment is as follows:
([Home Dataset](https://github.com/EnvGuard-2024/EnvGuard-2024.github.io/tree/master/DataSet/HomeEnvironment))

<p> 
We conducted a 14-day continuous data collection in the smart office and smart home, recording user activities, application executions and environment changes by capturing every event and action from the initial environment state. 
The spatial layout and the deployed devices of the smart office and the smart home are illustrated as follows:
<div align=center>
<img width="50%" style="margin-right:2%" src="https://raw.githubusercontent.com/EnvGuard-2024/EnvGuard-2024.github.io/master/images/SmartOfficeEnv.png"/>
<img width="47%" src="https://raw.githubusercontent.com/EnvGuard-2024/EnvGuard-2024.github.io/master/images/SmartHomeEnv.png"/>
</div>
</p>

<!-- There are 21 students working and studying in the laboratory, and 5 types of WoT applications are deployed to provide convenience for daily office work. Details of the applications are described below:
<div align=center><img width="400" src="https://raw.githubusercontent.com/EnvGuard-2024/EnvGuard-2024.github.io/master/images/application.png"/></div> -->
 
We deployed 5 types of WoT applications in office and home for our daily office work and home life. The applications are as follows:
<div align=center> 
<img width="44.6%" style="margin-right:2%" src="https://raw.githubusercontent.com/EnvGuard-2024/EnvGuard-2024.github.io/master/images/office_application.png"/>
<img width="48%" src="https://raw.githubusercontent.com/EnvGuard-2024/EnvGuard-2024.github.io/master/images/home_application.png"/> 
</div>

Through interviews with staff in the environment, we obtained ten expected safety and security property requirements from interviews with individuals who work or live there daily for each environment. We invited six experts with WoT development experience to independently analyze and label the events and actions that violated the properties (Fleiss Kappa = 0.68) and resolve discrepancies through discussion to obtain the ground truth. The properties are as follows:
<div align=center>
<img width="46%" style="margin-right:2%" src="https://raw.githubusercontent.com/EnvGuard-2024/EnvGuard-2024.github.io/master/images/office_propertys.png"/>
<img width="46.3%" src="https://raw.githubusercontent.com/EnvGuard-2024/EnvGuard-2024.github.io/master/images/home_propertys.png"/>
</div>

The dataset includes the initial state of the environment and devices, and the state changes during the following 14 days which are recorded in the formats: {Name, Type, Location, Object, Timestamp, Payload Data, Source, Property Violation, Resolving Action}. Name indicates the name of device service that provides information about changes in the state of the environment/device. Type represents the type (action or event) of the device service. Location indicates the deployment location of the device. Object denotes the state name of the target device/environment object being updated by the device service. Timestamp records  the time when the state change occurs. Source indicates that the data record is caused by an environment change, an application call, or an offline user operation. Payload Data records the current state value. Property Violation indicates the ID of violated environment properties caused by the device service. Resolving Action indicates the generated resolving strategy of the violation.
 
## GUI Tool
The visualized environment property description tool.([GUI](http://47.101.169.122:9033/))

## Environment Representations
The environment representation of the smart office WoT environment in [neo4j](http://47.101.169.122:7474/browser/)  (bolt port: `7687`, username: `neo4j`, password: `12345678`)

The environment representation of the smart home WoT environment in [neo4j](http://47.101.169.122:7475/browser/)  (bolt port: `7688`, username: `neo4j`, password: `12345678`)

## User Study 1
To understand the user preference for resolution actions, we conduct an online user study to analyze the correlation between the user-selected resolution action and the feature of the violation. The survey questionnair is as follows:
([User Study 1](https://github.com/EnvGuard-2024/EnvGuard-2024.github.io/blob/master/UserStudy/UserStudyOne_SurveyQuestionnair.docx))

## User Study 2
We invited 47 students (including 17 females) as participants with a variety of majors, including software engineering (21), biology (12), chemistry (9), and law (5). Among the participants, eighteen of them have experience using WoT platforms and developing WoT applications, while the others do not.  
The constructed properties of the office environment are as follows:
([Office-User Study 2](https://github.com/EnvGuard-2024/EnvGuard-2024.github.io/blob/master/UserStudy/UserStudyTwo_ConstructedProperties_Office.json))  
The constructed properties of the home environment are as follows:
([Home-User Study 2](https://github.com/EnvGuard-2024/EnvGuard-2024.github.io/blob/master/UserStudy/UserStudyTwo_ConstructedProperties_Home.json))

<!-- Properties of environments built by participants using visualisation development tools in usability user studies.([link](https://github.com/EnvGuard-2024/EnvGuard-2024.github.io/blob/master/user-study/user_study.json)) -->

