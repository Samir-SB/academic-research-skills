# Spatially Cohesive Service Discovery and Dynamic Service Handover for Distributed IoT Environments

**Authors**: Kyeong-Deok Baek and In-Young Ko  
**Affiliation**: School of Computing, Korea Advanced Institute of Science and Technology (KAIST), Daejeon, Republic of Korea  
**Publication**: ICWE 2017, LNCS 10360, pp. 60-78, 2017  
**DOI**: 10.1007/978-3-319-60131-1_4

---

## Abstract

The proliferation of the Internet of Things (IoT) enables the provision of diverse services that utilize IoT resources distributed in ad-hoc network environments. This has resulted in a new challenge, the issue of how to efficiently and dynamically discover appropriate IoT services that are necessary to accomplish a user task in the vicinity of the user. In this paper, we propose a service discovery method that finds IoT services from a user's surrounding environment in a spatially cohesive manner so that the interactions among the services can be efficiently carried out, and the outcome of service coordination can be effectively delivered to the user. In addition, to ensure a certain Quality of user Experience (QoE) level for the user task, we develop a service handover approach that dynamically switches from one IoT resource to an alternative one to provide services in a stable manner when the degradation of the spatial cohesiveness of the services is monitored. The spatio-cohesive service discovery and dynamic service handover algorithms are evaluated by simulating a mobile ad-hoc network (MANET) based IoT environment.

---

## 1. Introduction

Recent years have witnessed a wide spread proliferation of Internet of Things (IoT) and this has enabled the provision and deployment of diverse services that utilize IoT resources in urban environments. For effective collection of data and management of IoT services, recent commercial IoT-based systems, such as Microsoft Azure IoT Hub, have adopted the cloud computing model. However, owing to a rapid increase in the number of IoT resources in recent years, a centralized cloud computing model no longer remains scalable. Therefore, recent studies have suggested distributed computing models based on the Mobile Ad-hoc Network (MANET) to address the scalability issue. In this distributed model, IoT resources are accessible directly via a MANET, which allows for IoT resources to interact with each other in order to provide services to users in a more efficient and flexible manner without the need to deploy infrastructure. In addition, composite services can be developed by integrating IoT and other types of services such as Web and cloud services together to accomplish user tasks.

### Problem Statement

Such a distributed IoT environment raises a new challenge to efficiently and dynamically discovering appropriate IoT resources, which provides necessary IoT services to accomplish a user task, in the vicinity of the user. Several studies have been undertaken in the service-oriented architecture and Web services domains. In particular, mobility, location dependency, and composability of distributed services have been considered as important issues to address to enable effective service provision in practical IoT environments:

1. **Mobility**: Owing to mobility of users and IoT resources, the availability of IoT services frequently changes. Therefore, a discovery algorithm needs to dynamically discover valid IoT services that are necessary to perform user tasks.

2. **Spatial Location**: Unlike traditional Web services, the spatial location of a user and IoT resources affects the effectiveness of delivering IoT services to users. To deliver the outputs of IoT services to a user in an effective and efficient manner, corresponding IoT resources need to be located close to the user.

3. **Service Coordination**: Various services in an IoT environment need to coordinate with each other to perform complex user tasks, and therefore, cooperative IoT resources need to be located cohesively in a space where the user is located.

### Contribution

Even though there have been many studies on evaluating locational context of IoT services, none of them have focused on ensuring IoT resources that are involved with service coordination to be spatially cohesive to each other, to accomplish user tasks effectively. In this paper, we define **spatio-cohesive services** as services that utilize IoT resources that are located cohesively in a user's vicinity with the distance among the services short enough such that the outcome of the service coordination can be effectively delivered to the user.

The proposed approach consists of two phases:
1. **Service Discovery Plan Generation**: A service discovery plan is generated, which is a systematic plan for discovering services that can be coordinated together to accomplish a user task.
2. **Spatio-Cohesive Service Discovery and Handover**: IoT services are discovered and handed over using the service discovery plan.

---

## 2. Related Work

Service discovery in service computing environments can be classified into two types: **proactive** and **reactive** service discovery. Reactive service discovery algorithms discover services according to a user's request, while proactive service discovery algorithms discover services before a user's request based on advertisement from IoT resources. In distributed IoT environments, it is necessary to discover services in a reactive manner according to the requirements of user tasks because of scalability.

There have been various studies on scalable discovery of required services for performing user tasks in MANET environments. A MANET is an infrastructure-less environment, which can enable resources with high mobility to be connected with each other in a scalable manner. However, owing to the infrastructure-less characteristics of MANET, we cannot maintain a centralized service registry to discover services. Therefore, service discovery in a MANET needs to be performed in a decentralized manner.

With regard to delivering services to users while ensuring a high QoE, **context-aware service discovery** has been considered as an important issue in service provision. In these studies, contextual information such as a user's preferences and location are utilized to increase the integrated quality of discovered services from users' perspectives and in terms of the efficiency of network architecture. In particular, the location of services is a critical context that affects QoE in performing user tasks.

---

## 3. Spatially Cohesive Service Discovery and Dynamic Service Handover

### 3.1 Problem Definition

The spatio-cohesive service discovery and dynamic service handover problem is defined as follows. For a given task, T, the problem is to find a proper set of IoT resources, which are necessary to provide a set of required services, ST, of the task.

**Formal Definitions:**
- **Task (T)**: A description of a user's demand, which entails the services required to provide necessary functionalities.
- **Service Set (ST)**: The set of services required for task T.
- **Time Series (TS)**: A sequence of time instances, si, indicating a topology change of the MANET.
- **Network at time s (N(s))**: N(s) = (D ∪ {u}, E(s)) where D is the set of IoT resources and u is the user.
- **Vertex Position**: v:coord(s) returns the physical coordinate of the node at time s.
- **Spatio-cohesiveness Requirement**: (m, n, l) where m and n are a service or a user, and they need to be located spatially close to each other within an upper limit, l.

**Spatio-cohesiveness Achievement Measurement:**
```
ri(c) = max(1 - distancec(m, n)/l, 0)
```

**Spatio-cohesiveness Objective Function:**
```
RT(c) = Σs∈ST∪{u} min(ri(c)) / |ST ∪ {u}|
```

**Dynamic Service Handover Objective:**
```
handover(c(si-1), c(si)) = |c(si) - c(si-1)|
```

The problem is to find spatio-cohesive services for a user task while minimizing service handover cost throughout the lifecycle of the task.

### 3.2 Discovery Plan Generation

**Spatio-Cohesiveness Requirement Extraction:**
The spatio-cohesiveness requirements of a user task can be extracted automatically from a task template using an ontology model developed using Web Ontology Language (OWL). A Task has its own Task Template, which is composed of multiple Services. A service can have some Service Properties representing the quality attributes and constraints of the service.

**Spatio-cohesiveness Requirement Graph (SCRG):**
The spatio-cohesiveness requirements are represented as a graph called SCRG, in which the user and services are represented as vertices (ST ∪ {u}), and the spatio-cohesiveness requirements among them are represented as edges (RT).

**Discovery Plan Generation:**
A service discovery plan for a task, T, is defined as:
```
PT = (childP, nonChildP)
```
where childP is a subset of the spatio-cohesiveness requirements indicating the path in the requirement graph to discover child services from parent services.

Generation of the childP set is done by constructing a spanning tree of the SCRG. Various spanning tree algorithms such as Depth-First Search (DFS), Breadth-First Search (BFS), and Minimum Spanning Tree (MST) can be used.

### 3.3 Spatio-Cohesive Service Discovery and Handover

**Spatio-Cohesive Service Discovery:**
Based on the service discovery plan, the algorithm finds the IoT resources necessary to realize the services of a user task from the child services of the user node. Then, discovered services recursively find the resources for the child services.

The algorithm has two options:
1. **Concurrent service discovery**: Enable discovery of child services concurrently
2. **Multiple candidate services**: Find multiple candidate resources for a service

**Dynamic Service Handover:**
The major difference between traditional handover and service handover in an IoT environment is that service handover requires consideration of a set of services to perform a user task, while traditional handover considers only a single access point. The service handover algorithm monitors the spatio-cohesiveness status of the services and performs handover when some of the services are beyond the requirement boundary.

The handover decision rule uses a **hysteresis margin** and **threshold** to calculate the spatio-cohesiveness between:
- Resource of the parent service and the candidate resource
- Resource of the parent service and the current resource

---

## 4. Evaluation

### 4.1 Evaluation Setting

The simulations were performed using the NS3 simulator:
- **Environment**: 200 resource nodes deployed in a 100m × 100m rectangular area
- **Resource Coverage**: Approximately 7m × 7m area per resource
- **Mobility Model**: RandomDirection2d for mobile nodes, ConstantPosition for static nodes
- **Communication**: IEEE 802.11ac Wi-Fi channels with VhtMcs0 physical mode
- **Number of Services per Task**: 10 (medium complexity)
- **Velocity Range**: 1 m/s to 10 m/s (walking and running speed)
- **Simulation Duration**: 20 seconds per run, 50 repetitions per strategy

### 4.2 Evaluation Results

**Spatio-cohesiveness Results:**
- Without using a discovery plan: Poor spatio-cohesiveness because requirements between service pairs cannot be met
- Without handover algorithm: Continuous decrease in spatio-cohesiveness over time due to mobility
- With BFS/DFS + handover: High spatio-cohesiveness maintained even with mobile resources

**Options Comparison:**
- Enabling multiple candidate selections effectively reduces the number of service handovers
- Enabling concurrent service discovery reduces service discovery and handover time
- Using both options together results in the highest spatio-cohesiveness

**Service Priority Functions:**
- Using service priority functions helps improve spatio-cohesiveness, especially during handover
- Using the limit value of spatio-cohesiveness requirement results in more steady spatio-cohesiveness

---

## 5. Testbed Implementation

The testbed was implemented using:
- **Service Gateways**: Node-Red on Raspberry Pi 2 model B
- **IoT Resources**: Wemo Insight model F7C029de
- **User Device**: Android application for service discovery and task execution
- **Distance Measurement**: Received Signal Strength Indicator (RSSI)

**Demonstration Scenario:**
A "Make a pleasant environment for reading" task was demonstrated. As the user moves away from Light 1, the system detects degradation in spatio-cohesiveness and hands over the lighting service to Light 2, which is now closer to the user.

---

## 6. Conclusion

This paper proposed a service discovery method that finds IoT services from a user's surrounding environment in a spatially cohesive manner, and a service handover approach that dynamically switches from one IoT resource to an alternative one when degradation of spatio-cohesiveness is monitored.

**Key Contributions:**
1. Consideration of spatial inter-relationship among services and user to discover effective services
2. Systematic organization of services to be discovered and handed over based on spatial dependencies
3. Service handover algorithm reflecting complex handover situations associated with QoE of services

**Future Work:**
- Extend ontology model to represent diverse spatio-cohesiveness requirements and QoE conditions
- Extend algorithms to deal with unconnected SCRG to support any type of service coordination
- Study aspects of spatio-cohesiveness requirements as critical factors of QoE

---

## References

1. Gubbi, J., et al.: Internet of things (IoT): a vision, architectural elements, and future directions. Future Gener. Comput. Syst. 29(7), 1645-1660 (2013)
2. Corson, S., Macker, J.: Mobile ad hoc networking (MANET): routing protocol performance issues and evaluation considerations. No. RFC 2501 (1998)
3. Groba, C., Clarke, S.: Opportunistic service composition in dynamic ad hoc environments. IEEE Trans. Serv. Comput. 7(4), 642-653 (2014)
4. Jimenez-Molina, A., Ko, I.-Y.: Spontaneous task composition in urban computing environments based on social, spatial, and temporal aspects. Eng. Appl. Artif. Intell. 24(8), 1446-1460 (2011)
5. Truong, H.-L., Dustdar, S.: A survey on context-aware web service systems. Int. J. Web Inf. Syst. 5(1), 5-31 (2009)
6. Elgazzar, K., Hassanein, H.S., Martin, P.: Daas: cloud-based mobile web service discovery. Pervasive Mob. Comput. 13, 67-84 (2014)
7. Meshkova, E., et al.: A survey on resource discovery mechanisms, peer-to-peer and service discovery frameworks. Comput. Netw. 52(11), 2097-2128 (2008)
8. Sailhan, F., Issarny, V.: Scalable service discovery for MANET. In: Third IEEE International Conference on Pervasive Computing and Communications. IEEE (2005)
9. Chen, X., et al.: Web service recommendation via exploiting location and QoS information. IEEE Trans. Parallel Distrib. Syst. 25(7), 1913-1924 (2014)
10. Klein, A., Ishikawa, F., Honiden, S.: Towards network-aware service composition in the cloud. Proceedings of the 21st International Conference on World Wide Web. ACM (2012)