# EnvGuard-2023.github.io


## Datasets
We conducted a 14-day continuous data collection in a laboratory WoT environment, recording user activities, application executions and environment changes by capturing every event and action from the initial environment state. The spatial layout and the deployed devices of the environment are illustrated as follows:
<div align=center><img width="500" src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/layout.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/layout.png" width="500px"> -->
<!-- ![layout](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/layout.png) -->

There are 21 students working and studying in the laboratory, and 5 types of WoT applications are deployed to provide convenience for daily office work. Details of the applications are described below:
<div align=center><img width="400" src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/application.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/application.png" width="400px"> -->
<!-- ![application](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/application.png) -->

Through interviews with staff in the environment, we obtained ten environmental properties that are expected to be satisfied (listed in appendix), including five spatial state properties and five temporal trace properties. The properties are as follows:
<div align=center><img width="400" src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/propertys.png"/></div>
<!-- <img src="https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/propertys.png" width="400px"> -->
<!-- ![propertys](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/images/propertys.png) -->

In addition, we invited six experts with WoT development experience to independently analyze and label the events and actions that violated the properties (Fleiss Kappa = 0.68) and resolve discrepancies through discussion to obtain the ground truth.

[Dataset](https://EnvGuard-2023.github.io/dataset)

## GUI Tool
[The visualized environmental property description tool.](http://47.101.169.122:9033/)

## User Study 1
A study of user preferences for violation repair in WoT systems.([link](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/survey.docx))

## Environment Representations
The laboratory environment in [neo4j](http://1.117.166.48:7474/browser/)(bolt port: `7687`, no authentication)

## User Study 2
Properties of environments built by participants using visualisation development tools in usability user studies.([link](https://github.com/EnvGuard-2023/EnvGuard-2023.github.io/blob/master/user-study/user_study.json))

