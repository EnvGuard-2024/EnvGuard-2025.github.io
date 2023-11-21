# EnvGuard-2023.github.io


## Dataset
We collected data in a real-world WoT environment and built a dataset to evaluate EnvGuard. The dataset is publicly available.
([Dataset](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/tree/master/dataset))
We conducted a 14-day continuous data collection in a laboratory WoT environment, recording user activities, application executions and environment changes by capturing every event and action from the initial environment state. The spatial layout and the deployed devices of the environment are illustrated as follows:
<div align=center><img width="500" src="https://raw.githubusercontent.com/EnvGuard-2023/EnvGuard-2023.github.io/master/images/layout.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/layout.png" width="500px"> -->
<!-- ![layout](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/layout.png) -->

There are 21 students working and studying in the laboratory, and 5 types of WoT applications are deployed to provide convenience for daily office work. Details of the applications are described below:
<div align=center><img width="400" src="https://raw.githubusercontent.com/EnvGuard-2023/EnvGuard-2023.github.io/master/images/application.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/application.png" width="400px"> -->
<!-- ![application](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/application.png) -->

Through interviews with staff in the environment, we obtained ten environment properties that are expected to be satisfied (listed in appendix), including five spatial state properties and five temporal trace properties, and we invited six experts with WoT development experience to independently analyze and label the events and actions that violated the properties (Fleiss Kappa = 0.68) and resolve discrepancies through discussion to obtain the ground truth. The properties are as follows:
<div align=center><img width="400" src="https://raw.githubusercontent.com/EnvGuard-2023/EnvGuard-2023.github.io/master/images/propertys.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/propertys.png" width="400px"> -->
<!-- ![propertys](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/propertys.png) -->

The dataset includes the initial state of the environment and devices, and the state changes during the following 14 days which are recorded in the formats: {Name, Type, Location, Object, Timestamp, Payload Data, Source, Conflict, Fix, Method}. Name indicates the name of device service that provides information about changes in the state of the environment/device. Type represents the type (action or event) of the device service. Location indicates the deployment location of the device.  Object denotes the state name of the target device/environment object being updated by the device service. Timestamp records  the time when the state change occurs. Payload Data records the current state value. Conflict indicates the ID of violated environment properties caused by the device service. Fix indicates the generated resolving strategy of the violation, and Method denotes the way to fix the device service (Undo or Resolve).

## GUI Tool
The visualized environment property description tool.([GUI](http://47.101.169.122:9033/))

## User Study 1
To understand the user preference for resolution actions, we conduct an online user study to analyze the correlation between the user-selected resolution action and the feature of the violation. The survey questionnair is as follows:
([User Study 1](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/UserStudyOne_SurveyQuestionnair.docx))
<!-- A study of user preferences for violation repair in WoT systems.([link](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/survey.docx)) -->

## Environment Representations
The environment representation of the smart laboratory WoT environment in [neo4j](http://47.101.169.122:7474/browser/)(bolt port: `7687`, username: `neo4j`, password: `12345678`)

## User Study 2
We invite all of the 21 students (including 8 females) as participants who are familiar with the laboratory environment to specify the ten environment properties through the property configuration tool. The constructed properties are as follows:
([User Study 2](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/UserStudyTwo_ConstructedProperties.json))
<!-- Properties of environments built by participants using visualisation development tools in usability user studies.([link](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/user_study.json)) -->

