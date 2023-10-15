# EnvGuard-2023.github.io


## Dataset
We collected data in a real-world WoT environment and built a dataset to evaluate EnvGuard. The dataset is publicly available.
([Dataset](https://EnvGuard-2023.github.io/dataset))

We conducted a 14-day continuous data collection in a laboratory WoT environment, recording user activities, application executions and environment changes by capturing every event and action from the initial environment state. The spatial layout and the deployed devices of the environment are illustrated as follows:
<div align=center><img width="500" src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/master/images/layout.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/layout.png" width="500px"> -->
<!-- ![layout](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/layout.png) -->

There are 21 students working and studying in the laboratory, and 5 types of WoT applications are deployed to provide convenience for daily office work. Details of the applications are described below:
<div align=center><img width="400" src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/master/images/application.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/application.png" width="400px"> -->
<!-- ![application](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/application.png) -->

Through interviews with staff in the environment, we obtained ten environment properties that are expected to be satisfied (listed in appendix), including five spatial state properties and five temporal trace properties, and we invited six experts with WoT development experience to independently analyze and label the events and actions that violated the properties (Fleiss Kappa = 0.68) and resolve discrepancies through discussion to obtain the ground truth. The properties are as follows:
<div align=center><img width="400" src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/master/images/propertys.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/propertys.png" width="400px"> -->
<!-- ![propertys](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/propertys.png) -->

The dataset consists of attributes: {Name, Type, Location, Object, Timestamp, Payload Data, Source, Conflict, Fix, Method}, where Name means the name of the device service, Type means the type(action or event) of the device service, Location means the location where the device service occurs, Object means the object where the device service occurs, Timestamp means the time when the device service occurs, Payload Data means the time when the device service occurs, Source denotes the source of the device service, Conflict means the conflict caused by the device service, Fix means the possible fixing behavior of the device service, and Method means the way to fix the device service(Undo or Resolve).

## GUI Tool
The visualized environment property description tool.([GUI](http://47.101.169.122:9033/))

## User Study 1
To understand the user preference for resolution actions, we conduct an online user study to analyze the correlation between the user-selected resolution action and the feature of the violation. The survey questionnair is as follows:
([User Study 1](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/survey.docx))
<!-- A study of user preferences for violation repair in WoT systems.([link](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/survey.docx)) -->

## Environment Representations
The environment representation of the smart laboratory WoT environment in [neo4j](http://1.117.166.48:7474/browser/)(bolt port: `7687`, username: `neo4j`, password: `12345678`)

## User Study 2
We invite all of the 21 students (including 8 females) as participants who are familiar with the laboratory environment to specify the ten environment properties through the property configuration tool. The constructed properties are as follows:
([User Study 2](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/user_study.json))
<!-- Properties of environments built by participants using visualisation development tools in usability user studies.([link](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/user_study.json)) -->

