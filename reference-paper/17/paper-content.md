This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                   1




          A Deep Reinforcement Learning Approach for
               Composing Moving IoT Services
                             Azadeh Ghari Neiat, Athman Bouguettaya, Fellow, IEEE, Mohammed Bahutair

                 Abstract—We develop a novel framework for efficiently and effectively discovering crowdsourced services that move in close
                 proximity to a user over a period of time. We introduce a moving crowdsourced service model which is modelled as a moving
                 region. We propose a deep reinforcement learning-based composition approach to select and compose moving IoT services
                 considering quality parameters. Additionally, we develop a parallel flock-based service discovery algorithm as a ground-truth
                 to measure the accuracy of the proposed approach. The experiments on two real-world datasets verify the effectiveness and
                 efficiency of the deep reinforcement learning-based approach.

                 Index Terms—IoT, mobile crowdsourcing, mobile IoT services, moving crowdsourced service, service composition, deep
                 reinforcement learning, MapReduce, crowdsourced IoT service, spatio-temporal mapper, mobile computing.

                                                                                                     F



         1       I NTRODUCTION                                                                                                  Crowdsourced Moving Hotspot Services
                                                                                                                                               WiFi Service




         T       H e crowdsharing economy is an emerging dynamic
               ecosystem where people create new on-demand ser-
         vices through sharing or exchanging resources to achieve
         mutually beneficial goals [1]. This new type of economy
         has the potential to be applied in a diverse range of
         sectors, including tourism and hospitality, labor and service
         platforms, mobility and logistics [2]. Two well-known
         examples of are Uber 1 and Airbnb 2 . The foundations of
                                                                          WiFi hotspot service
         this emerging economy are anchored in crowdsourcing and               consumer
                                                                                               WiFi hotspot service
                                                                                                    provider
         crowdsharing [3]. In crowdsourcing environments, crowds
         need a medium to interact and produce results. A wide
                                                                            Fig. 1. WiFi Hotspot Sharing Scenario.
         variety of devices are used to facilitate certain types of
         crowdsourcing [4], [5]. In particular, Internet of Things ple of such services is a WiFi hotspot provided by a person
         (IoT) devices are usually used to allow the crowd to provide through their smartphone. This type of crowdsourced IoT
         and use services. We define services as an abstraction that services is characterised by their spatio-temporal aspects.
         transforms IoT data into actionable information [6]. In The spatio-temporal properties refer to the location/space
         that respect and more formally, a service is defined by and time/period in which crowdsourced services are pro-
         its functional and non-functional attributes. A functional visioned and consumed. We use moving IoT service and
         attribute is usually defined as what a service provides, i.e., mobile IoT service interchangeably.
         the purpose of the service. Non-functional attributes are               Mobility is an important and intrinsic part of the non-
         qualities attached to service provisioning, i.e., Quality of       functional          aspect of crowdsourced services. The mobility of
         Service (QoS). For example, a functional attribute of an           IoT     devices        provides opportunities to dynamically extend
         airline service is reservation. A non-functional attribute of      service         coverage          to larger spaces and at flexible times.
         this service is the price which would be attached to the           Mobility,           however,          presents key challenges in terms of
         reservation.                                                       qualitative         factors       (e.g., availability) if the aim is to provide
            A moving crowdsourced IoT service is a service provided         users       with     the    best      quality of experience. In this respect,
         by an IoT device moving in time, space, or both. An exam-          we     focus       on   the   spatio-temporal      aspects as key parameters
                                                                            to query moving crowdsourced services.
                                                                                 We identify two key types of crowdsourced services with
         • A. Ghari Neiat is with the School of Information Technol-
            ogy, Deakin University, Geelong, VIC 3220, Australia Email:     regard       to spatial location: fixed and moving. A fixed crowd-
            azadeh.gharineiat@deakin.edu.au.                                sourced service refers to services which are permanent in
            A. Bouguettaya and M. Ba-Hutair are with the School of          space during the time period of the service provisioning.
            Computer Science, University of Sydney, Darlington, NSW
            2008, Australia. E-mail: athman.bouguettaya@sydney.edu.au and   For example, Diana may share her WiFi hotspot while she
            mbah6158@uni.sydney.edu.au.                                     is sitting at a coffee shop. In contrast, moving crowdsourced
            1. www.uber.com                                                 service is not tied to any specific location at any point in
            2. www.airbnb.com                                               time. For example, Diana may share her WiFi hotspot as


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                   2



         she moves from one location to another when strolling in                                        degrade dramatically as the dataset scales up. As a result,
         the city. More specifically, we assume that a fixed hotspot                                     creating and maintaining an index in parallel computing
         service will remain available (in terms of time and location)                                   like MapReduce cannot be effective [20]. To address this
         when selected by a service consumer and throughout the                                          we propose a pruning approach that aims at diverting the
         provisioning of the service. However, for moving hotspot                                        algorithm from selecting invalid services without the need
         services, the availability and location can change during                                       to index them.
         service provisioning. Additionally, crowdsourced services                                          The contribution of the paper is summarized as follows:
         have another dimension, i.e., they may also be deterministic                                        • We propose a spatio-temporal model for moving
         or non-deterministic. A crowdsourced IoT service is Deter-                                            crowdsourced IoT services. Our previous work in [25]
         ministic if time period and availability at a certain location                                        and [26] proposed a selection and composition model
         are known in advance. A crowdsourced IoT service is Non-                                              for fixed crowdsourced services based on spatio-
         deterministic if time period and location availability are not                                        temporal features. We also proposed a temporal non-
         known in advance.                                                                                     deterministic service discovery approach. In this work,
            There has been a large body of research on service selec-                                          we focus on deterministic moving services.
         tion and composition in mobile environment [7], [8], [9],                                           • We design a novel solution based on deep reinforce-
         [10]. Most existing methods focus on service selection and                                            ment learning to support effective discovery and com-
         composition based on Quality of Service (QoS) parameters                                              position without using an index.
         [11] and energy consumption [12], [13]. They do not take                                            • We devise a ground-truth, called parallel flock-based
         into account the mobility of a user or service provider.                                              moving crowdsourced service discovery, using Apache
         There are only a few works that address the mobility-aware                                            Spark. This is used to measure the accuracy of the
         service selection problem [14], [15]. However, these works                                            proposed discovery model in terms of service discov-
         do not consider the composition of mobile IoT services                                                ery in each timestep. The algorithm is based on a
         while both IoT service provider and consumer are moving                                               spatio-temporal MapReduce. After the spatio-temporal
         together.                                                                                             filtering is conducted, we retrieve the valid candidates
            We identify the following research challenges. The first                                           and feed them to our deep reinforcement learning-
         challenge is connectivity which is an intrinsic part of                                               based composition approach.
         moving crowdsourced service discovery. A moving service                                             • We conduct a set of extensive experiments on two
         should stay connected with a service provider, i.e., be                                               real datasets. The results show the efficiency and
         within connectivity proximity of the provider. This requires                                          effectiveness of the approach in terms of accuracy,
         determining co-movement patterns. We propose a parallel                                               learning speed and scalability in comparison with the
         flock-based service discovery to find co-movement services.                                           ground-truth.
         The parallel flock-based approach is based on a spatio-
         temporal MapReduce to efficiently find flock patterns [16].                                        The rest of the paper is organized as follows: Section
         We first apply a temporal map step to prune sub-trajectories                                    2 surveys related work. Section 3 introduces our system
         of moving services with regards to a user trajectory. We                                        model and states the problem of crowdsourced moving
         then deploy a spatial map step to filter candidate moving                                       service composition. Section 4 presents the deep rein-
         services which are located within a circular region of a                                        forcement learning-based composition algorithm. Section 5
         user trajectory. The second challenge is service conti-                                         provides the ground-truth approach. Section 6 reports our
         nuity to connect to the next moving service as an IoT                                           experimental results. Section 7 concludes the related work
         service provider and a user is not necessarily sharing all                                      and highlights future work.
         their route. Therefore, an effective composition approach
         is required to select an optimal set of available moving
                                                                                                         Motivation Scenario
         crowdsourced services which ensure the service continuity.
         Most existing trajectory similarity joins approaches are                                        Scenario 1: WiFi tethering may be a connection option
         time-interval based [17], [18] and their methods are not                                        when free public WiFi is not available or effective due
         applicable to continuous temporal matching as they retrieve                                     to low connection speed and limited capacity. In WiFi
         approximate results. Little work [19] addresses the issue                                       tethering, the crowd can switch on their IoT devices’ WiFi
         of continuous nearest neighbour joins on big trajectory                                         hotspot and share their data balance to other devices for
         datasets. The key difference with our approach is the need                                      some rewards. As a result, WiFi hotspot can be crowd-
         to select continuous sub-trajectories considering a range                                       sourced. IoT devices can be anything the crowd has and
         of QoS parameters. We propose a Deep Reinforcement                                              is connected to the Internet. Generally, IoT devices can be
         Learning-based composition algorithm to find and compose                                        divided into two main categories: fixed and mobile. Fixed
         valid candidate moving services which overlap with the                                          IoT devices are referred to devices that typically do not
         user trajectory. Third challenge is indexing. Existing co-                                      move, e.g., smart fridge, smart TV, etc. Mobile devices are
         movement discovery methods usually rely on centralized                                          devices that are inherently made to be carried by people,
         index methods like R-tree. [20] shows that the performance                                      such as smartwatches, and smartphones. Wearables are a
         of the existing co-movement discovery methods like flock                                        subset of mobile IoT devices. They are special IoT devices
         [16], convoy [21], swarm [22], group [23] and platoon [24]                                      that are meant to be worn (e.g., smart shoes and smart


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                   3



         shirts). It is predicted that wearables in the near future                                      are tasks that require specific spatial attributes from the
         would become ubiquitous [27].                                                                   crowd for successful task fulfillment. For example, spatial
            We consider WiFi hotspot sharing as one of the repre-                                        tasks may require the crowd to be physically located at
         sentatives of crowdsourced IoT services. For instance, it                                       certain locations and collect data. Others may require the
         can be leveraged to offer a range of crowdsourced services                                      crowd to move between different locations to fulfill their
         such as WiFi-coverage travel planning for cost-effective                                        task. Crowdsourcing spatial tasks are often referred to
         media streaming. In this regard, crowdsourced WiFi hotspot                                      as Mobile Crowdsourcing. Mobile crowdsourcing typically
         services are provided by smartphones which are moving in                                        involves a crowd with mobile devices (e.g., smartphones
         space and time through a mobile application. For example,                                       and smartwatches) to satisfy the spatial requirements by the
         Open Garden3 created an application that lets users share                                       tasks. There have been several works in the area of mobile
         and consume the Internet among each other. They use a                                           crowdsourcing. In this section we focus on two types of
         monetary incentive, where providers set the price per MB                                        mobile crowdsourcing: (1) spatial crowdsourcing [5], [31],
         and consumers pay according to their usage.                                                     and (2) urban crowdsourcing [32], [33].
            The trajectories of the services are deterministic. De-                                          In spatial crowdsourcing, the outsourced tasks are typi-
         terministic trajectories refer to the a-priori knowledge of                                     cally designated with specific locations. The crowd should
         the trajectories. It is assumed that there is a platform that                                   execute the tasks at the specified locations. CrowdSens-
         incentivizes WiFi hotspot providers to move to specified                                        ing@Place (CSP) [34] is one example of spatial crowd-
         areas and share their resources [28]. Therefore, the WiFi                                       sourcing. CSP aims at labeling places into categories (e.g.,
         hotspot providers are assumed to follow certain trajecto-                                       cafe or restaurants). It leverages spatial data, user trajec-
         ries that have been assigned. In particular, we focus on                                        tories, and sampled audio clips and images to achieve
         the trajectories of pedestrians. We also assume that WiFi                                       this. Another framework is proposed in [35] that tries
         hotspot services will overlay digital maps. We propose to                                       to find a suitable set of users to answer location-based
         reformulate the research problem of moving crowdsourced                                         queries. Location-based services (e.g., Foursquare) are used
         IoT service selection and composition as finding the optimal                                    to answer queries instead of relying on spatial task as-
         composition of WiFi hotspot moving services which provide                                       signments to users. It is worth noting that despite many
         the best quality of experience to fulfill users’ specific                                       works proposed on spatial crowdsourcing, there has been
         requirements/expectations (e.g., watching online videos and                                     little attention to spatio-temporal crowdsourcing.
         signal strength) (Fig. 1).                                                                          Urban crowdsourcing aims at detecting users’ transporta-
            Scenario 2: Providing convenient power to IoT users is                                       tion modes using collected spatio-temporal and acceleration
         a valuable service to help them to stay connected. Wire-                                        data [32]. The work in [36] and [37] proposes mobile
         less energy transfer technologies [29] transforms the way                                       crowdsourcing approaches that use commuters trajectories
         people charge their IoT devices and enables energy sharing                                      to predict real-time arrival of buses. A new platform,
         between mobile IoT devices seamlessly from a distance. We                                       namely OneBusAway, is proposed in [38] to predict the
         consider crowdsourcing energy as a service scenario which                                       real-time arrival time of buses. OneBusAway collects users’
         has the potential to create a green environment [30]. For                                       comments and feedback through Twitter, blogs and bug
         example, someone wearing smartshoes that have generated                                         trackers. Another approach is proposed in [39] to accu-
         energy through walking can share the harvested green                                            rately identify the right crowdsourced sensors to answer
         energy with other IoT devices wirelessly within a range.                                        a particular journey planning request. In particular, an
         This can also enable users to recharge their smartphones as                                     unsupervised learning approach is introduced to select and
         they move.                                                                                      cluster the right mobile crowdsourced sensors based on
                                                                                                         common patterns in their trajectories.
         2       R ELATED W ORK                                                                              We investigate in our work the concept of mobile crowd-
                                                                                                         sourced services that combines mobile crowdsourcing and
         We provide an overview of the relevant research in relation
                                                                                                         the service paradigm. We show that mobile crowdsourced
         to the selection and composition of crowdsourced moving
                                                                                                         services offer more efficient techniques for processing
         services. We first present a review of mobile crowdsourcing
                                                                                                         spatio-temporal sensor data.
         frameworks. We then review previous studies on service
         composition. Finally, we survey co-movement discovery
         approaches.                                                                                     2.2 Service Composition
                                                                                                         Mobile crowdsourcing aspires to provide a platform where
         2.1 Mobile Crowdsourcing                                                                        moving users act as service providers offering crowd-
         Crowdsourcing aims at outsourcing tasks to the crowd                                            sourced services for a smart city. Only a few studies have
         for faster and efficient execution. Crowdsourced tasks                                          focused on crowdsourcing as a service [8], [40], [41],
         may require specific requirements compared to others.                                           [42]. For example, in [8] a CrowdService framework is
         For example, computing tasks require the crowd to have                                          developed to provide crowd worker and crowd intelligence
         computers with enough processing power. Spatial tasks                                           as crowd services via mobile crowdsourcing. A composition
                                                                                                         approach is developed based on Genetic Algorithm (GA) to
             3. https://opengarden.com                                                                   provide near-optimal composite services. [43] introduces a


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing
                                                                                    𝑹𝒔
                                           y
                                                time
         IEEE TRANSACTIONS ON SERVICES COMPUTING                                  (𝑥𝑠 , 𝑦𝑠 ,t s )                                                                                                  4
                                                                            x

         crowdsourced service platform called sensing as a service                                                                                                       (𝑥𝑒 , 𝑦𝑒 , 𝑡𝑒 )
         (S 2 aaS). In this platform, mobile service providers or
         smartphone users can request sensing services if they have
         fulfilled previous sensing tasks [44]. Furthermore, several
         crowdsourced service composition frameworks have been                                                          y                   𝒓

         proposed to select and compose crowdsourced services. In                                                               time
                                                                                                                                          (𝑥𝑠 , 𝑦𝑠 ,t s )
         [45], an agent-based crowd service composition framework                                                                   x
         is proposed in a scenario of purchasing a secondhand
         laptop. The framework takes into account users’ constraints                                     Fig. 2. Moving crowdsourced service model.
         including the response time and the cost to select and                                          equilibrium and fictitious play process to ensure the con-
         compose crowdsourced services. A crowdsourced service                                           vergence of the agent to a unique equilibrium. The previous
         framework is proposed for composing energy services [15].                                       approaches are applied in web service composition. In
         A new temporal composition algorithm which is a variation                                       contrast, our approach is based on spatio-temporal aspects
         of a fractional knapsack algorithm is developed to compose                                      of moving IoT services.
         crowdsourced energy services to satisfy a user’s energy
         requirement. However, the studies above assume that the
         crowdsourced services are fixed in space and time.                                              2.3 Co-Movement Discovery
            A service composition approach is proposed in [11]                                           There exist many studies to discover similar co-movement
         while considering the service’s QoS and mobility. The                                           patterns including flock [54], [16], convoy [21], swarm [22]
         mobility-aware QoS notion is built using the service invo-                                      and moving clusters [55]. A flock pattern refers to a group
         cations’ mobility model, which describes the performance                                        of at least m > 1 objects moving together within a user-
         of a service. On the other hand, only one QoS criterion                                         defined disk with radius r for at least k > 1 consecutive
         i.e., location-sensitive response time is taken into account                                    timestamps. In the flock pattern discovery, moving objects
         to select an optimal service composition plan in [9] and                                        are clustered based on a disk-based region. A key challenge
         [11]. A Mobile Service Sharing Community (MSSC) is                                              in flock pattern is the selection of proper disk size. Larger
         proposed in [9] for moving service users and providers.                                         disk size may capture wrong objects and a smaller radius
         Additionally, a composition approach for mobile service                                         may miss some objects. To overcome this challenge, a
         is introduced based on Krill-Herd algorithm for finding                                         convoy pattern is introduced to cluster moving objects
         optimal response time. In [14], a mobility-aware service                                        using a density-based clustering method like DBSCAN
         selection approach is proposed that takes into account a                                        [56]. Instead of staying within a disk, moving objects of a
         user’s movement path. The selection algorithm is modelled                                       convoy are connected based on the density. While flock and
         based on GA and simulated annealing algorithm. The                                              convoy patterns have a temporal consecutiveness constraint,
         proposed approach reduces the response time of the service                                      swarm and moving cluster patterns relax this constraint
         request by selecting appropriate edge servers as the user                                       through accepting short-term deviations. However, it is not
         moves. A three-tier IoT service composition framework that                                      required to have unique (i.e., same) objects throughout the
         takes into account spatio-temporal and energy constraints                                       timestamps in moving cluster pattern. Swarm, group [23]
         is proposed in [13]. In this framework, an IoT service                                          and platoon [24] adopt different pruning techniques relying
         composition algorithm is developed that adopts GA, Ant                                          on depth-first search which are not efficient in parallel
         Colony Optimization, and Particle Swarm Optimization to                                         processing [20]. Most existing methods rely on centralized
         find an optimal composition plan while reducing network                                         indexing methods built on top of the whole dataset which
         energy consumption. In contrast to the above studies, we                                        may not be effective and efficient in parallel computing
         propose a service composition approach where both service                                       [20]. We focus on the parallel discovery of moving flock
         provider and user are moving together.                                                          patterns without using an indexing method.
            There are some composition approaches that integrate
         service selection and compositions with Reinforcement
                                                                                                         3  S YSTEM M ODEL AND P ROBLEM F ORMU -
         Learning RL [46], [47], [48]. In [49], a novel multicriteria-
         driven reinforcement learning algorithm is proposed for                                         LATION
         dynamic Web service composition which adapts Random-                                            In this section, we first formally model crowdsourced
         ized Reinforcement Learning (RRL) [50]. The proposed                                            moving services by moving regions. We then formulate
         approach enables continuous adjustment of the service com-                                      the problem of selecting and composing the best candidate
         position through learning about the quality of new services                                     moving services with respect to their deterministic behavior.
         and exploring new composition plans while optimizing
         multiple criteria and satisfying users’ constraints. There are
                                                                                                         3.1 Problem Formulation
         two RL-based service composition algorithms [51], [52]
         which are not efficient for large scale service composition.                                    Definition 1: Moving Crowdsourced Service M S. A mov-
         In [53], a new model for the large-scale adaptive service                                       ing crowdsourced service M S is a tuple of < id, F , Q >
         composition based on Multi-Agent Reinforcement Learning                                         where
         (MARL) is introduced. The model utilizes the coordination                                         • id is a unique service identifier,



1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                     5



             •  F is a function offered by M S, e.g., providing a                                                                       𝑢𝑡3                     𝑢𝑡4
                moving WiFi hotspot. The function of the moving                                                                                                           𝑢𝑡5

                service represents a moving service’s coverage in                                                           𝑢𝑡2
                                                                                                                                                                                           𝑢𝑡6

                space and time. We define the coverage as a moving
                                                                                                                                  𝑆2
                region which is described by a tuple of < Ts , Rti (pi )
                                                                                                                  𝑢𝑡1
                > where
                  – Ts is a service trajectory which is a sequence of
                     timestamped samples {< ti , xi , yi >, 1 ⩽ i ⩽ k},
                     where xi is longitude and yi is latitude and ti is
                     a timestamp.                                                                                                 Points of a user’s trajectory 𝑇𝑢    Points of moving service 𝑀𝑆1

                  – Rti (pi ) is the specific coverage region that is                                                             Points of moving service M𝑆2        Points of moving service 𝑀𝑆3
                     offered by M S. Without loss of generality, the
                     moving region is represented by a circular area                                     Fig. 3. An example of valid candidate moving services.
                     which is centered at pi with the radius r at ti ,                                         each user’s trajectory point to find overlapped services.
            • Q is a set of QoS attributes qi ( e.g., capacity).                                            • The maximum spatial proximity equals the radius of
            Fig. 2 shows a moving crowdsourced service model in a                                              fixed WiFi hotspot coverage (e.g., 20 m).
         3D space.                                                                                          • We focus on deterministic moving crowdsourced ser-
            Definition 2: User Trajectory Tu . A user trajectory is                                            vices. A deterministic environment can be achieved
         the path that is traveled by a user which is a set of k time-                                         using several incentive-based approaches (e.g., [57],
         stamped samples Tu ={ < uti , uxi , uyi >, 1 ⩽ i ⩽ k }.                                               [58], [59], [60], [28]. For example, our work in [28]
            Definition 3: Spatial Candidate Pair. Given a set of mov-                                          proposes a framework that encourages the movement
         ing services > = {M S1 , M S2 , ..., M Sn }, a user trajectory                                        of crowdsourced IoT service providers from over-
         Tu = {up1 , up2 , ..., upn } where upi =( uxi , uyi ), a search                                       supplied regions to under-supplied regions.
         radius rs , a moving service is formed as a spatial candidate                                      Problem Definition. Given a set of moving crowd-
         pair cpti for a given timestep ti if its location M Sk .pi at ti                                sourced services > = {M S1 , M S2 , ..., M Sn }, a user
         is inside a disk region Dti (center = upi (ti ), radius = rs ).                                 trajectory Tu and a search radius rs as input, the prob-
         The service is inside the disk if the Euclidean or Harvestine                                   lem is formulated as finding the “optimal” composition
         distance d(Tu .upi , M Sk .pi ) between two points of user tra-                                 plan that gives the best trade-offs among multiple QoS
         jectory Tu .uptii and service trajectory M Sk .ptii at timestep                                 criteria i.e., a high QoS while maintaining a low number
         ti is less than rs . Without loss of generality, our method can                                 of disconnections. The output is a composition plan CP
         be extended for other distance metrics including network                                        which is a sequence of moving crowdsourced services
         distance and Manhattan distance. The range distance r                                           CP = {S1 , S2 , ..., Sn } if f Si is a valid candidate moving
         reflects the maximum spatial proximity allowed.                                                 service for a given user trajectory (see Definition 4).
            Definition 4: Valid Candidate Moving Service. A moving
         service M Si is a valid candidate service for a given user                                      3.2 QoS Model for Moving Crowdsourced Service
         trajectory if it is paired with the user trajectory over                                        A key challenge is to find a service that offers a better qual-
         w consecutive timesteps, where w > 0, i.e., CM Si =                                             ity due to the diversity of moving services. QoS parameters
         {cpta , cpta , ...cptw }, ta < tb < ... < tw and |a − b| = 1.                                   are used to distinguish among moving services. It is worth
            For example, in Fig. 3, we plot six timestep snapshots                                       noting that the proposed quality model is extensible. A new
         of a user moving in an arbitrary trajectory. Spatio-temporal                                    QoS parameter (either generic or domain-specific) may be
         neighbour search of a user trajectory at timestep ut4 is                                        added without fundamentally altering the underlying com-
         M S1 and M S2 , while M S3 is not a valid candidate moving                                      putation mechanisms. For example, in the crowdsourced
         service. Services in spatial proximity of a user are grouped                                    energy service scenario, we could use energy-related QoS
         in circles.                                                                                     parameters including Transmission Success Rate and De-
            We use the following assumptions in our problem for-                                         liverable Energy Capacity which are proposed in [30] to
         mulation:                                                                                       distinguish among energy services. In our WiFi hotspot
            • One moving service can only serve one user at any                                          scenario, we use one quality attribute that we proposed in
                point in time.                                                                           [25] capacity.
            • A moving service moves between any two consecutive                                            Capacity (cap): Capacity represents the maximum for the
                timestamps ti and ti+1 with a constant speed. As a                                       information transmission data rate. SNR Shannon-Hartley
                result, we can determine the position of the moving                                      theorem [61] is used to model the capacity. In our model,
                service at any given time in the time interval [ti , ti+1 ].                             the capacity is directly proportional to the signal strength.
                As long as the function of finding the moving service’s                                  The better signal strength is, the higher Signal-to-Noise-
                location is constant time, other speed functions could                                   Ratio (SNR) i.e., less error is. We assume that the error
                be considered.                                                                           rate is fixed. Hence, increasing the capacity increases the
            • Radii of all coverage regions of services are fixed to a                                   signal strength, which leads to more successful transmis-
                single value. Therefore, we consider the region around                                   sions. Given a moving crowdsourced service M S, qcap is


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                   6



                                                                                                         selection in real-time may disrupt the user experience for
                                                                                                         consumers. For example, if we assume a consumer that
                                                     (𝑀𝑆. 𝑥, 𝑀𝑆. 𝑦)                                      wishes to use a WiFi hotspot for watching videos. The
                                                                                                         playback may be interrupted every now and then whenever
                                                              (𝑢𝑥, 𝑢𝑦)                                   the device is looking for a new service. Therefore, we
                                                                                                         opt for ahead of time service selection to minimize the
                                                                                                         interruption overhead.
         Fig. 4. Strength Model.                                                                            One single moving service may not fully cover a user
         computed as follows.                                                                            trajectory as the user may not necessarily share their entire
                                   B                                                                     route with said moving service. As a result, we need
                                    qcap =
                                      log2 (1 + str)             (1)                                     to compose candidate moving services to satisfy a user’s
                                   K
                                                                                                         requirements and ensure service continuity. In this section,
            where B is the total available bandwidth and K is the
                                                                                                         we present our approach for selecting and composing all
         maximum number of concurrent requests that a moving
                                                                                                         candidate moving services. We leverage Deep Reinforce-
         service M S can support. Total available bandwidth is
                                                                                                         ment Learning DRL to find and compose valid candidate
         assumed to be equally allocated between different IoT
                                                                                                         services overlapping with the user trajectory. Reinforce-
         service users. Signal strength str represents the sensing
                                                                                                         ment Learning is a subclass of machine learning, where
         region of a moving crowdsourced service. The strength is
                                                                                                         an agent learns about an environment’s behavior through
         computed based on the distance between the user trajectory
                                                                                                         explorations. The main reason for our choice to DRL is its
         point Tu .pi = (ux, uy) and the moving service point
                                                                                                         ability to discover the ”cumulative” optimal set of service
         M S.pi = (M S.x, M S.y) at timestep ti . For instance, as
                                                                                                         trajectories, given the trajectory segments of a user. The
         the user moves closer to the WiFi hotspot, the perceived
                                                                                                         DRL does that by assigning rewards for every action the
         WiFi signal gets stronger. The str is based on the expo-
                                                                                                         agent invokes. In our work, the actions are the service
         nential attenuation probabilistic coverage model [62] which
                                                                                                         segments that a user can use. The agent’s role is to pick
         is computed as follows.
                                                                                                         the next service segment that would maximize the overall
                                                                                                         reward. Therefore, the agent should not only consider the
                   
                       1     0 ⩽ pdis(Tu .pi , M S.pi ) ⩽ Rc
                                                                 (2)                                     current service and user trajectory segments to make the
                     e−kd      pdis(Tu .pi , M S.pi ) > Rc
                                                                                                         selection but also future service and user segments. DRL
            where d         =     pdis(Tu .pi , M S.pi ) − Rc and                                        offers a way for the agent to predict the ”future” (i.e.,
         pdis(Tu .pi , M S.pi ) is the perpendicular distance from                                       unknown knowledge) by learning the behavior of the envi-
         the crowdsourced service center point M S.pi to a user                                          ronment through explorations. The agent is the composition
         trajectory point Tu .pi (Fig. 4). Rc is a confident radius                                      algorithm which determines the optimal combination of
         and k is a decay factor which determines the rate of                                            candidate moving services over time. An environment is
         the signal attenuation with regard to the distance. Rc                                          characterized by its set of states (S) and actions (A). In
         and k parameters can have different values based on the                                         our work, the environment is the combination of service
         sensor types and the operation environment which can be                                         trajectories and a single user trajectory, (see Fig. 5). A
         obtained through experiments. The strength str is within                                        user trajectory consists of a series of samples i.e. states.
         the range of (0,1]. If the user trajectory point is within the                                  Each sample is a tuple: < ut, ux, uy >, where ut is
         distance of Rc , the strength is 1 which means full signal.                                     the timestamp, ux is the longitude coordinate, and uy is
         In the interval (Rs − Rc ) where Rs = pdis(Tu .pi , M S.pi ),                                   the latitude coordinate. The services trajectories dataset
         the value of str exponentially approaches zero as the                                           comprises a series of records representing different samples
         perpendicular distance increases. In our model, str 6= 0                                        < t, x, y > for different services. A sample in the services
         because a valid candidate crowdsourced service point is                                         trajectories dataset contains the same information as a user
         paired with a user trajectory point which means that the                                        trajectory sample with the addition of a service ID and
         value of pdis is not beyond Rs (Fig. 4).                                                        QoS attributes (see Definition 1). At any given time, the
            The QoS value of a full composite moving crowdsourced                                        environment has a current state s ∈ S i.e. the current
         IoT service is computed by calculating the average of the                                       user trajectory sample that is reported to the agent. The
         capacities of all its component moving services.                                                agent selects an action (a ∈ A) i.e., a valid candidate
                                                                                                         moving IoT service to invoke on the environment. Upon
         4  D EEP  R EINFORCEMENT    L EARNING -                                                         action invocation, the environment generates a reward (r)
                                                                                                         based on the action and its current state. Additionally, the
         BASED C OMPOSITION A LGORITHM
                                                                                                         environment changes its state according to the invoked
         The proposed framework aims at finding the optimal service                                      action and previous state. The reward and next state are
         composition for a given moving consumer. The framework                                          reported back to the agent i.e., composer.
         neither assumes nor requires consumers to change their                                             More formally, we define a composite moving service as
         trajectories for better services. Simply put, the composition                                   follows.
         plan is obtained by identifying the set of services that                                           Definition 5: Composite Moving Crowdsourced Service.
         intersects with the consumer’s trajectory. Performing the                                       A composite moving service CS is a sequence of com-


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                   7




                                                                                                                     (d.2) The environment fetches next user’s trajectory
                                                                                                                     sample as the next state.

                                           (a) The agent requests the initial state & a list of available (b.1) The environment fetches the first user’s sample
                                           candidate moving services from the environment.                 and sends it to the agent as the initial state.




                                                                                                                                                    Users’ Trajectories
                                                                                                                                                         𝑢𝑡1 , 𝑢𝑥1 , 𝑢𝑦1




                                                                                                                  Environment
                                                                                                                                                         𝑢𝑡2 , 𝑢𝑥2 , 𝑢𝑦2
                                                                                                                                                                …
                                                                                                                                                         𝑢𝑡𝑛 , 𝑢𝑥𝑛 , 𝑢𝑦𝑛
                                       Agent

                                                   (c) Perform an action by selecting a moving service ID.

                                                                                                                                                  Services Trajectories
                                                                                                                                                       𝑡1,1 , 𝑥1,1 , 𝑦1,1
                                                   (e) The environment sends the computed reward and                                                   𝑡1,2 , 𝑥1,2 , 𝑦1,2
                                                   next state to the agent.                                                                            𝑡2,1 , 𝑥2,1 , 𝑦2,1
                                                                                                                                                               …
                                                                                                                                                       𝑡𝑝,𝑛 , 𝑥𝑝,𝑛 , 𝑦𝑝,𝑛




                                                                                                                  (b.2) The environment fetches the candidate moving
                                                                                                                   service IDs and passes them as actions to the agent.

                                                                                                                  (d.1) The environment checks the moving service samples
                                                                                                                  with the selected moving service ID. The environment
                                                                                                                  also computes the reward based on the current state's x
                                                                                                                  and y, and the selected moving service's x and y.




         Fig. 5. Reinforcement learning for moving crowdsourced service composition.


         ponent moving services, which is defined as a 5-tuple of                                        follows:
         < S g , sg0 , sgr , Ag (s), Rg > where                                                                                                π ∗ (s) = a                                      (3)
                   g
             • S is a finite set of states i.e., samples < t, x, y > that                                where s ∈ S is the environment’s state and a ∈ A is an
               are observed by an agent g;                                                               optimal moving service (i.e., action) to invoke. Obtaining
                 g        g
             • s0 ∈ S       is the initial state of the agent g and                                      the optimal policy is achieved by solving the Q-value
               the execution of the composite moving service starts                                      function:
               from this state. Here the initial state is the first user                                                              X
               trajectory sample.                                                                               Q(s, a) = r(s, a) + γ     max
                                                                                                                                            0
                                                                                                                                               Qi (s0 , q 0 )|s, a (4)
                 g        g                                                                                                                                      a
             • sr ⊂ S       is the set of terminal states where the                                                                                     s0
               execution of a composite service terminates upon                                          where Q(s, a) is the accumulated QoS reward, given an
               arriving at one of the states. The terminal state is the                                  agent starting at state s and invoking action a, r(s, a) is
               last sample of a user trajectory.                                                         the instantaneous reward when invoking action a at state s,
                  g
             • A (s) is the set of actions that are taken at each state                                  and γ is a discounting factor.
               s. Here we replace the actions with valid candidate                                          Finding the optimal policy directly using Equation 4 is
               moving services (see Definition 4). At each state, we                                     impractical due to a potentially large number of states and
               have a set of moving services that could be selected                                      actions. As a result, the number of state-action combina-
               and executed.                                                                             tions increases drastically which in turn leads to exponential
                  g
             • R is the reward function when a moving service is                                         time complexity. Therefore, Neural Networks are used in
               invoked. There are multiple QoS objectives which the                                      conjunction with Equation 4 to build a policy model. The
               agent wants to achieve. The user receives the reward                                      use of Neural Networks to find the optimal policy is referred
               i.e., desired QoS when the agent moves to the next                                        to it as Q-Learning. The inputs to the Neural Network are
               state s from s0 . Therefore, the reward is computed                                       the different parameters defining a particular state s, and
               using the QoS of a composite service.                                                     its outputs are all possible actions that the agent can take.
           The composition algorithm aims at finding the optimal                                            Q-learning has two main phases: exploration and ex-
         policy (π ∗ ) which is defined as the procedure for selecting                                   ploitation. In the exploration phase, the agent selects ran-
         candidate moving services (i.e., the action to be invoked by                                    dom actions and keeps records of the resulting rewards and
         the agent in each state). This guides the agent toward an                                       next states. The collected records are then fed into a Neural
         optimal set of moving services that gives the best trade-offs                                   Network to train the policy. During the exploitation phase,
         among multiple QoS criteria i.e., maximum accumulated                                           the agent uses the trained model to predict the next action
         reward. More formally, the optimal policy is expressed as                                       to take. It is worth noting that in the exploitation phase,


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                  8


  User
Trajectory       Moving services
                                                                                                                 Candidate pairs    Candidate moving services
                                     𝑢𝑡!                                                                 𝑢𝑡!       𝑀𝑆" , 𝑀𝑆#          𝑇& 𝑀𝑆! 𝑀𝑆" 𝑀𝑆#
                                                                                                                                      𝑢𝑡!
                                     𝑢𝑡"                                                                 𝑢𝑡"       𝑀𝑆! , 𝑀𝑆"
                                                                                                                                      𝑢𝑡"
                                   … 𝑢𝑡#                                                                 𝑢𝑡#     𝑀𝑆! , 𝑀𝑆" , 𝑀𝑆#
                                                                                                                                      𝑢𝑡#
                                     𝑢𝑡$                                                                 𝑢𝑡$        𝑀𝑆" , 𝑀𝑆#         𝑢𝑡$
                                     𝑢𝑡%                                            𝑟                    𝑢𝑡%       𝑀𝑆" , 𝑀𝑆#          𝑢𝑡%


                                                        …
               𝑀𝑆! 𝑀𝑆"   𝑀𝑆# 𝑀𝑆$


             (a) RDD: dataset                   (b) Temporal mapper            (c) Spatial mapper              (d) Reduce by key            (e) Candidate set


Fig. 6. Workflow of parallel flock-based moving crowdsourced service discovery.

Algorithm 1 Reinforcement Learning-based Composition                        reward based on the invoked action. We set the reward as
Training Algorithm                                                          the QoS provided by the selected candidate moving service
Input: A set of sampled moving service trajectories Ts , a                  (step (d.1)). The environment updates its current state by
set of sampled user trajectories Tu , and the radius r                      setting it to the next user trajectory sample (step (d.2)). The
Output: A model for policy π                                                next state and reward are sent to the agent (step (e)). The
 1: // Initialization                                                       agent continues invoking actions until all samples in the
 2:  ← 1.0                                                                 user trajectories are visited. Upon traversing all samples of
 3: model ← create an initial neural network model                          a user trajectory, the environment resets itself (by setting
 4: memory ← []                                                             its state to the first user trajectory sample), and the process
 5: env ← initialize environment using Ts                                   repeats. Note that several user trajectories should be used
 6: // Model Training                                                       to increase the prediction accuracy of the generated model.
 7: for tu ∈ Tu do                                                             Two cases have not been addressed in our previous
 8:      for i ← 1 to repetition do                                         scenario: (1) no valid candidate moving services for a given
 9:          env.current user = tu                                          user trajectory sample, and (2) an agent selects a moving
10:          state ← tu                                                     service that is not a valid candidate (i.e., does not overlap
11:          if random() <  then                                           either in time or space with the current user trajectory
12:              action ← pick a random service id from Ts                  sample). To resolve the first case, we introduce the concept
13:          else                                                           of a dummy service. A dummy service essentially means
14:              action ← predict the next action using                     that there are no valid candidate moving services for a
    model and state                                                         particular user trajectory sample. The goal of a dummy
15:          end if                                                         service is to divert the agent from selecting an invalid
16:          reward, next state ← act on env using                          candidate moving service when no overlapping services are
    action                                                                  found. Accomplishing this is carried out by giving a lower
17:          store next state and reward in memory                          reward value whenever the dummy service is selected, e.g.,
18:      end for                                                            -1 as opposed to [0 - 1] for normal reward values. Resolving
19:      if memory is full then                                             the second case is achieved by penalizing the agent when
20:          train model using data in memory                               an invalid moving service is selected, e.g., -10. By this, an
21:           = ∗0.995 // gradually decreasing exploration                agent will always favor selecting the dummy service over
22:      end if                                                             an invalid one since it has a higher reward value.
23: end for                                                                    Algorithm 1 summarizes the training phase of the ap-
24: return model                                                            proach. The algorithm starts by initializing the parameters
the agent keeps exploring to adjust the trained model for                   (Lines 1-5). Initially, the reinforcement learning agent per-
higher accuracies.                                                          forms exploration only. The exploration to exploitation ratio
                                                                            is controlled by changing  (1.0 for full exploration and 0.0
   Fig. 5 summarizes the process. An agent starts by                        for full exploitation). A neural network model is created
requesting the initial state of the environment (step (a)).                 with random weights in Line 3. The algorithm also ini-
The environment fetches the first user trajectory sample                    tializes an empty space that represents the agent’s memory
and reports it as its current state (step (b.1)). Additionally,             (Line 4). The memory stores information that the agent
the environment fetches the list of service IDs and reports                 collects during exploration. More specifically, the memory
them to the agent as possible actions to invoke (step (b.2)).               holds every action the agent takes on the environment.
During exploration, the agent randomly invokes an action                    Additionally, it stores the rewards the environment assigns
(by selecting a valid candidate moving service ID) on                       for the taken actions. Finally, the environment is set up
the environment (step (c)). The environment computes the                    using the provided service trajectories Ts (Line 5). The


     Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                   9



         environment uses the service trajectories Ts to determine                                       [63]. All of these group movement patterns require the
         its set of possible actions as well as the reward for each                                      group to contain the same set of individuals during its
         taken action.                                                                                   lifetime [64]. We opt for the flock pattern as it is the
            The model is trained gradually while the agent is ex-                                        most appropriate group movement pattern to describe our
         ploring the environment and exploiting its current model                                        WiFi hotspot sharing scenario due to the fixed size of
         (Lines 7 through 21). The agent at the beginning favors                                         the radius (i.e., WiFi hotspot range). However, other co-
         exploring the environment over exploiting its model. The                                        movement patterns may be more appropriate for other types
         algorithm loops through each user trajectory in Ts (Line                                        of applications.
         7). The state of the environment is set using the samples
         in a given user trajectory. When the agent takes an action,                                     Algorithm 2 Parallel Flock-Based Service Discovery Al-
         the environment sets its next state to the next sample in                                       gorithm
         the current user trajectory. We allow the environment to                                        Input: A set of moving services ς , A user travel trajectory
         exploit each user trajectory repetition times (Lines 8 - 10).                                   Tu , Radius r
         In other words, a state can be repeated several times. This                                     Output: A set of spatial candidate pairs
         allows the agent to experiment with different actions given
                                                                                                          1: C ← {}
         the same state, and observe the rewards associated with
                                                                                                          2: compute a list of < ti ,STti > pairs of ς
         each state-action combination. The agent invokes an action
                                                                                                          3: compute a list of timesteps < uti ,Tupi > pairs of Tu
         on the environment (Lines 11 - 15). The action is the service
                                                                                                          4: – Temporal Mapper Phase–
         to choose given a user trajectory sample. The taken action
                                                                                                          5: for all key-value pairs < ti ,STti > do
         is based on the value of . The agent tends to take random
                                                                                                          6:     left outer join based on timesteps uti
         actions when  has a high value (exploration). Conversely,
                                                                                                          7: end for
         the agent uses its trained model to decide which action to
                                                                                                          8: – Spatial Mapper Phase –
         take. Upon each invoked action, the environment changes
                                                                                                          9: for all ti in key-value pairs < ti ,STpi > do
         its state and returns a reward to the agent (Line 16). The
                                                                                                         10:     find spatial candidate pairs based on r and Tupi
         reward is generated based on the QoS of the selected service
                                                                                                         11: end for
         (i.e., the taken action). The reward and next state values are
                                                                                                         12: – Reduce Phase–
         stored in memory (Line 17). The collected actions, states,
                                                                                                         13: group-by uti
         and rewards in memory are used to train the model (Line
                                                                                                         14: Return spatial candidate pairs set
         20). In other words, memory guides the training process
         towards building a model that favors actions with higher
         rewards. The value of  is decayed after each training                                              We deploy a parallel moving service discovery approach.
         process (Line 21). Decaying  makes the agent use the                                           We use Apache Spark as a platform for parallel discovery.
         trained model more, essentially leading the agent to invoke                                     The Apache Spark employs MapReduce to handle the scal-
         actions that may have higher rewards.                                                           ability and fault tolerance issues. Fig. 6 shows MapReduce
            It is worth mentioning that model training and storage is                                    jobs which are performed in a sequential workflow. First,
         carried out using edge servers. We assume edge servers                                          the temporal map phase conducts temporal pruning of
         are conveniently set up to be accessed by moving IoT                                            moving services with regards to a user trajectory. In this
         services. Each edge server is responsible for serving a                                         temporal mapper, timestamp and sampled location are re-
         small subset of moving devices. Therefore, storage and                                          spectively treated as key and value for each moving service
         processing overheads are negligible.                                                            trajectories. Since a user trajectory is important to find the
                                                                                                         co-movement service, we filter moving service trajectories
                                                                                                         based on a user trajectory’s timesteps. In this regard, we
         5 G ROUND -T RUTH : PARALLEL F LOCK -
                                                                                                         use left outer join as a temporal filtering step to select all
         BASED M OVING S ERVICE D ISCOVERY                                                               moving services that include the user trajectory timesteps
         We propose a brute-force approach to find the optimal                                           (Lines 5-7 Algorithm 2). Second, for each timestep of a
         composition of moving services for a given consumer                                             user trajectory, the spatial map phase is performed over all
         trajectory. Our approach is used in our experiments to                                          filtered sub-trajectories of moving services. In the spatial
         evaluate the accuracy of our deep reinforcement learning-                                       mapper, we retrieve all spatial candidate service pairs (see
         based composition algorithm proposed earlier. In other                                          Definition 2) whose points are inside a range distance r
         words, the brute-force approach acts as a ground-truth                                          of the user location point in each timestep. Finally, the
         (baseline) to validate the results obtained using the deep                                      spatial mapper outputs candidate pairs in each timestep
         reinforcement learning-based algorithm.                                                         of the user trajectory. It is represented by a list of key-
            The brute-force is the optimal solution as it performs                                       value pairs < uti , STi >, where uti is the user’s timestep
         exhaustive search to find all possible co-moving services                                       and STi is a set of candidate moving service IDs that
         with a given consumer’s trajectory. We achieve this by iden-                                    are paired at uti (Lines 9-11 Algorithm 2). For each
         tifying co-movement patterns. Several studies have been                                         discovered candidate pairs, QoS values are computed. We
         proposed to model moving objects including flock [54],                                          then extend the discovered candidate pairs to discovered
         [16], convoy [21], swarm [22] and travelling companion                                          candidate moving services. All candidate moving services


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                  10



                                                                                                         neurons each. The rectified linear unit (ReLU) activation
                           100                                                                           function is used in all hidden layers. We use dropout with
                           90                                                                            probability 0.5 on all hidden layers to reduce overfitting.
                           80                                                                            The Q-learning’s discount factor γ is set to 0.9, whereas
                           70                                                                            the Neural Network’s learning rate is 0.001.
                           60                                                                               The reward function used by the deep learning-based
              Accuracy %




                                                                                         Accuracy        composition algorithm is based on the capacity QoS param-
                           50                                                            Error
                           40                                                                            eter. We assume that the Q-learning algorithm does not have
                           30
                                                                                                         prior knowledge about QoS attributes of moving services
                           20
                                                                                                         since they are computed based on the distance between a
                                                                                                         user and a moving service. As a result, we rely on the Q-
                           10
                                                                                                         Learning algorithm to learn the optimal execution policy.
                            0
                             100     200   300 400 500 600 700 800                       900    1000     We use 70% of the data in each dataset for the training set
                                           Number of User Trajectories During Training
                                                                                                         and the remaining 30% for the test set.
                                                                                                            We use two real pedestrian trajectory datasets. A single
         Fig. 7. Accuracy on the indoor dataset
                                                                                                         trajectory in the datasets is represented with a series of
                                                                                                         location samples. Each sample represents the location of a
                                                                                                         person at a specific time. We use the trajectories in the two
                           100                                                                           datasets to represent WiFi hotspot moving services and user
                                      Accuracy                                                           trajectories4 . The trajectories in the datasets are split into
                           90         Error
                           80                                                                            two groups. The first group represents the available WiFi
                           70
                                                                                                         hotspot moving services. The second group is considered
                                                                                                         as the trajectories of the users. Throughout our experi-
                           60
                                                                                                         ments, we use our proposed algorithm to perform service
                           50
              %




                                                                                                         selection and composition using the moving services and
                           40
                                                                                                         user trajectories groups. In other words, for a given user
                           30
                                                                                                         trajectory, our proposed algorithm aims at finding a subset
                           20                                                                            of moving services that intersect with the user trajectory
                           10                                                                            while maximizes the QoS. The two datasets are described
                            0                                                                            as follows:
                                 5   10     15    20      25      30       35      40     45        50
                                           Number of User Trajectories During Training                                  5
                                                                                                            • Indoor : The dataset keeps visitors’ trajectories in the
                                                                                                               ATC shopping center in Osaka. The visitors’ locations
         Fig. 8. Accuracy on Illinois dataset.                                                                 are sampled every 0.03 - 0.06 seconds. In this dataset,
                                                                                                               we replace sampled timestamps with global sequences
         are validated based on Definition 3 and invalid candidates
                                                                                                               that start from 1 to find co-movement patterns. A fixed
         are disregarded.
                                                                                                               sampling rate of 0.04 seconds is set, since trajectories
                                                                                                               do not have synchronized sampled time. We adopt
         6          E XPERIMENTAL E VALUATIONS                                                                 linear interpolation to fill missing points. The dataset
         We evaluate the accuracy and efficiency of our proposed                                               contains 1,777,297,164 samples and 185,554 trajecto-
         deep reinforcement learning-based composition algorithm.                                              ries i.e. moving services.
                                                                                                                         6
         We utilize our ground-truth approach discussed earlier to                                          • Illinois : The dataset holds six months trajectories

         validate the results and assess the accuracy of our algorithm.                                        from the daily commute of two members in Argonne
         We leverage real pedestrian trajectory datasets throughout                                            National Laboratory of the University of Illinois at
         our experiments.                                                                                      Chicago. Each trajectory shows a continuous daily
                                                                                                               trip of a member in Cook County and/or the Dupage
                                                                                                               County of Illinois. We treat each trajectory as a
         6.1 Experiment Setup                                                                                  moving service. The member’s locations are strictly
         All experiments are conducted in a cluster with six nodes                                             sampled every second. There are 357,706 samples and
         on Amazon Web Services. We pick one master node and                                                   207 trajectories i.e. moving services.
         five slave nodes. The master node has a dual-core processor                                        To the best of our knowledge, there is limited research
         with 4GB memory. The slave nodes are identical, each                                            investigating QoS-aware moving IoT service composition.
         equipped with a 16-core processor and 64GB memory. We                                           We compare the proposed deep reinforcement learning-
         configure the cluster into 15 Spark executors, each taking                                      based composition algorithm to the proposed ground-truth
         19GB memory and 5 cores.                                                                        approach to show the accuracy of the selection process.
            We use a dense fully connected network to train our
                                                                                                           4. To the best of our knowledge, there are no publicly available
         model. The inputs to the network are the parameters                                             crowdsourced hotspot/energy environment datasets.
         defining a state whereas the outputs are the actions, which                                       5. https://irc.atr.jp/crest2010 HRI/ATC dataset
         the agent can take. Three hidden layers are used with 512                                         6. https://www.cs.uic.edu/ boxu/mp2p/gps data.html


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                     Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                                      11




                                                                                                                                             104

                                                                                                                                             103
                Time (log seconds)




                                                                                                                       Time (log seconds)
                                     104                                                                                                     102

                                                                                                                                             101


                                     103                                                                                                     100

                                                                          Ground-truth Computation Time                                                                           Ground-truth Computation Time
                                                                          Q-Learning Training Time                                          10 1
                                                                                                                                                                                  Q-Learning Testing Time
                                       100   200   300 400 500 600 700 800                       900   1000                                    100   200    300 400 500 600 700 800                      900   1000
                                                   Number of User Trajectories During Training                                                              Number of User Trajectories During Testing

         Fig. 9. Computation time vs. No. of user trajectories.                                                     Fig. 10. Computation time vs. No. of user trajectories.
         6.2 Experiments results
         In this section, we evaluate our deep reinforcement
         learning-based composition algorithm from three aspects:                                                                           35000
         (1) accuracy; (2) scalability and (3) efficiency of learning.
                                                                                                                                            30000
         Accuracy
                                                                                                                                            25000
         In the first set of experiments, we study the accuracy of the
                                                                                                                         Time (seconds)

         deep reinforcement learning-based composition algorithm                                                                            20000
         by comparing it to the ground-truth approach on two
         real datasets. We evaluate the accuracy of the proposed                                                                            15000
         approach by comparing the deep reinforcement learning-
         based composition algorithm in selecting valid candidate                                                                           10000

         moving services in each timestep and their corresponding                                                                            5000
         valid candidate moving services that are retrieved by the                                                                              10000 20000 30000 40000 50000 60000 70000 80000 90000 100000
                                                                                                                                                                  Number of Service Trajectories
         ground-truth. The accuracy is the ratio between the number
         of times an optimal service was selected cs to the total                                                   Fig. 11. Convergence time vs. No. of moving services.
         number of available valid samples ns.
                                                                               |cs|                                 selection computation time. Fig. 9 demonstrates the ground-
                                                       Accuracy =                                             (5)   truth computation time in comparison with the Q-learning
                                                                               |ns|
                                                                                                                    model training time. As expected, the results show that the
            Fig. 7 shows the accuracy (blue curve) and error (orange
                                                                                                                    ground-truth computation time is significantly lower than
         curve) of the deep reinforcement learning-based composi-
                                                                                                                    the training time. On the other hand, Fig. 10 illustrates
         tion algorithm on indoor dataset while varying the number
                                                                                                                    the computation time to find valid candidate services of
         of user trajectories from 100 to 1,000. As mentioned earlier,
                                                                                                                    deep reinforcement learning-based composition algorithm
         the accuracy (and error) results are obtained by validat-
                                                                                                                    significantly outperforms the ground-truth (i.e. less than 0.1
         ing the proposed approach results with the ground-truth
                                                                                                                    Sec in Q-learning in comparison with close to 10,000 Sec
         approach, which generates the best possible composition
                                                                                                                    in ground-truth for 1000 services). This indicates that the
         plan (i.e., accuracy 100%). The results show the proposed
                                                                                                                    deep reinforcement learning-based composition algorithm
         approach scores high accuracy. As can be seen, the accuracy
                                                                                                                    can select valid candidates much faster than the spatio-
         significantly increases until it reaches around 95% by 500
                                                                                                                    temporal MapReduce approach.
         user trajectories and then it remains stable. As expected,
         the accuracy is lower when the number of trajectories is
         low. The reason is that the lower the samples are, the                                                     Efficiency of learning
         less accurate the result is. Similarly, Fig. 8 shows that                                                  In the third set of experiments, we study the learning speed
         the accuracy (blue curve) and error (orange curve) of the                                                  with increasing the number of moving services on indoor
         composition algorithm on the Illinois dataset. The accuracy                                                and Illinois datasets. Firstly, we vary the number of moving
         increases until it reaches a high accuracy of around 93%                                                   services from 10,000 to 100,000 on the indoor dataset. The
         after 35 user trajectories.                                                                                results in Fig. 11 illustrate how fast the algorithm converges
                                                                                                                    to the optimal composition plan during the learning phase.
         Scalability                                                                                                The convergence time increases polynomially with the
         In the second set of experiments, we evaluate the scala-                                                   increasing number of moving services which is an expected
         bility of the proposed approach in terms of training and                                                   result. This is because the number of candidate moving


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                   Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                  12



                                                                                                         [6]  A. Bouguettaya, M. Singh, M. Huhns, Q. Z. Sheng, H. Dong, Q. Yu,
                                1800                                                                          A. G. Neiat, S. Mistry, B. Benatallah, B. Medjahed et al., “A service
                                                                                                              computing manifesto: the next 10 years,” Communications of the
                                1600                                                                          ACM, vol. 60, no. 4, pp. 64–72, 2017.
                                1400                                                                     [7] E. Badidi, Y. Atif, Q. Z. Sheng, and M. Maheswaran, “On personal-
                                                                                                              ized cloud service provisioning for mobile users using adaptive and
                                1200                                                                          context-aware service composition,” Computing, vol. 101, no. 4, pp.
               Time (seconds)




                                                                                                              291–318, 2019.
                                1000                                                                     [8] X. Peng, J. Gu, T. H. Tan, J. Sun, Y. Yu, B. Nuseibeh, and
                                800
                                                                                                              W. Zhao, “Crowdservice: optimizing mobile crowdsourcing and
                                                                                                              service composition,” ACM Transactions on Internet Technology
                                600                                                                           (TOIT), vol. 18, no. 2, pp. 1–25, 2018.
                                                                                                         [9] S. Deng, L. Huang, J. Taheri, J. Yin, M. Zhou, and A. Y. Zomaya,
                                400                                                                           “Mobility-aware service composition in mobile communities,” IEEE
                                                                                                              Transactions on Systems, Man, and Cybernetics: Systems, vol. 47,
                                200
                                       50   70        90            110           130   150                   no. 3, pp. 555–568, 2017.
                                                 Number of Service Trajectories                          [10] P. K. D. Pramanik and P. Choudhury, “Mobility-aware service provi-
                                                                                                              sioning for delay tolerant applications in a mobile crowd computing
         Fig. 12. Convergence time vs. No. of moving services.                                                environment,” SN Applied Sciences, vol. 2, no. 3, pp. 1–17, 2020.
                                                                                                         [11] S. Deng, L. Huang, D. Hu, J. L. Zhao, and Z. Wu, “Mobility-
                                                                                                              enabled service selection for composite services,” IEEE Transactions
         services that should be searched at each state increases                                             on Services Computing, vol. 9, no. 3, pp. 394–407, 2016.
                                                                                                         [12] Z. Zhou, D. Zhao, L. Liu, and P. C. Hung, “Energy-aware compo-
         exponentially. Additionally, the convergence time increases                                          sition for wireless sensor networks as a service,” Future Generation
         slower than the number of moving services. Secondly, we                                              Computer Systems, vol. 80, pp. 299–310, 2018.
         vary the number of moving services from 50 to 150 on the                                        [13] M. Sun, Z. Zhou, and Y. Duan, “Energy-aware service composition
                                                                                                              of configurable iot smart things,” in 2018 14th International Confer-
         Illinois dataset. Fig. 12 shows that the convergence time                                            ence on Mobile Ad-Hoc and Sensor Networks (MSN). IEEE, 2018,
         increases with increasing the number of moving services.                                             pp. 37–42.
         The results also show that our model trains relatively fast                                     [14] H. Wu, S. Deng, W. Li, J. Yin, X. Li, Z. Feng, and A. Y. Zomaya,
                                                                                                              “Mobility-aware service selection in mobile edge computing sys-
         to find optimal composition plans (e.g., less than 30 min                                            tems,” in 2019 IEEE International Conference on Web Services
         for 150 services).                                                                                   (ICWS). IEEE, 2019, pp. 201–208.
                                                                                                         [15] A. Lakhdari, A. Bouguettaya, S. Mistry, and A. G. Neiat, “Com-
                                                                                                              posing energy services in a crowdsourced iot environment,” IEEE
                                                                                                              Transactions on Services Computing, 2020.
         7           C ONCLUSION                                                                         [16] J. Gudmundsson and M. van Kreveld, “Computing longest duration
         We proposed a crowdsourced IoT service framework to                                                  flocks in trajectory data,” in Proceedings of the 14th annual ACM
                                                                                                              international symposium on Advances in geographic information
         select and compose moving crowdsourced IoT services                                                  systems. ACM, 2006, pp. 35–42.
         based on spatio-temporal factors. We developed a deep rein-                                     [17] R. Vernica, M. J. Carey, and C. Li, “Efficient parallel set-similarity
         forcement learning-based algorithm to select and compose                                             joins using mapreduce,” in the 2010 ACM International Conference
                                                                                                              on Management of data SIGMOD. ACM, 2010, pp. 495–506.
         moving services considering QoS parameters without using                                        [18] X. Zhang, L. Chen, and M. Wang, “Efficient multi-way theta-join
         an index. We also developed a spatio-temporal MapReduce                                              processing using mapreduce,” Proceedings of the VLDB Endowment,
         based on flock patterns using Apache Spark to discover                                               vol. 5, no. 11, pp. 1184–1195, 2012.
                                                                                                         [19] Y. Fang, R. Cheng, W. Tang, S. Maniu, and X. Yang, “Scalable
         moving services as a ground-truth. Our experiments show                                              algorithms for nearest-neighbor joins on big trajectory data,” IEEE
         the scalability and high accuracy of the proposed approach                                           Transactions on Knowledge and Data Engineering, vol. 28, no. 3,
         in comparison with the ground-truth. In our future work, we                                          pp. 785–800, 2016.
                                                                                                         [20] Q. Fan, D. Zhang, H. Wu, and K.-L. Tan, “A general and parallel
         develop and test our proposed approach on different motion                                           platform for mining co-movement patterns over large-scale trajec-
         patterns, i.e., transportation modes. We also plan to ex-                                            tories,” Proceedings of the VLDB Endowment, vol. 10, no. 4, pp.
         tend the proposed framework to temporal non-deterministic                                            313–324, 2016.
                                                                                                         [21] H. Jeung, M. L. Yiu, X. Zhou, C. S. Jensen, and H. T. Shen,
         moving services.                                                                                     “Discovery of convoys in trajectory databases,” Proceedings of the
                                                                                                              VLDB Endowment, vol. 1, no. 1, pp. 1068–1080, 2008.
                                                                                                         [22] Z. Li, B. Ding, J. Han, and R. Kays, “Swarm: Mining relaxed tem-
         R EFERENCES                                                                                          poral moving object clusters,” Proceedings of the VLDB Endowment,
                                                                                                              vol. 3, no. 1-2, pp. 723–734, 2010.
         [1]       E. L. Nekaj, “The crowd economy: From the crowd to businesses to                      [23] Y. Wang, E.-P. Lim, and S.-Y. Hwang, “Efficient mining of group
                   public administrations and multinational companies,” in Crowdfund-                         patterns from user movement data,” Data & Knowledge Engineering,
                   ing for Sustainable Entrepreneurship and Innovation. IGI Global,                           vol. 57, no. 3, pp. 240–282, 2006.
                   2017, pp. 1–19.                                                                       [24] Y. Li, J. Bailey, and L. Kulik, “Efficient mining of platoon patterns
         [2]       A. Taeihagh, “Crowdsourcing: a new tool for policy-making?”                                in trajectory databases,” Data & Knowledge Engineering, vol. 100,
                   Policy Sciences, vol. 50, no. 4, pp. 629–647, Dec 2017. [Online].                          pp. 167–187, 2015.
                   Available: https://doi.org/10.1007/s11077-017-9303-3                                  [25] A. G. Neiat, A. Bouguettaya, T. Sellis, and S. Mistry, “Crowdsourced
         [3]       J. Howe, “The rise of crowdsourcing,” Wired magazine, vol. 14,                             coverage as a service: two-level composition of sensor cloud ser-
                   no. 6, pp. 1–4, 2006.                                                                      vices,” IEEE Transactions on Knowledge and Data Engineering,
         [4]       J. A. Burke, D. Estrin, M. Hansen, A. Parker, N. Ramanathan,                               vol. 29, no. 7, pp. 1384–1397, 2017.
                   S. Reddy, and M. B. Srivastava, “Participatory sensing,” Center for                   [26] A. G. Neiat, A. Bouguettaya, and T. Sellis, “Spatio-temporal com-
                   Embedded Network Sensing, 2006.                                                            position of crowdsourced services,” in Internation Conference on
         [5]       L. Kazemi and C. Shahabi, “Geocrowd: enabling query answering                              Service-Oriented Computing (ICSOC). Springer, 2015, pp. 373–
                   with spatial crowdsourcing,” in Proceedings of the 20th International                      382.
                   Conference on Advances in Geographic Information Systems. ACM,                        [27] S. Seneviratne, Y. Hu, T. Nguyen, G. Lan, S. Khalifa, K. Thi-
                   2012, pp. 189–198.                                                                         lakarathna, M. Hassan, and A. Seneviratne, “A survey of wearable


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                      Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                  13



              devices and challenges,” IEEE Communications Surveys & Tutorials,                          [48] K. Gai and M. Qiu, “Reinforcement learning-based content-centric
              vol. 19, no. 4, pp. 2573–2620, 2017.                                                            services in mobile sensing,” IEEE Network, vol. 32, no. 4, pp. 34–39,
         [28] A. G. Neiat, A. Bouguettaya, and S. Mistry, “Incentive-based                                    2018.
              crowdsourcing of hotspot services,” ACM Transactions on Internet                           [49] I. J. Jureta, S. Faulkner, Y. Achbany, and M. Saerens, “Dynamic
              Technology (TOIT), vol. 19, no. 1, pp. 1–24, 2019.                                              web service composition within a service-oriented architecture,” in
         [29] W. Na, J. Park, C. Lee, K. Park, J. Kim, and S. Cho, “Energy-                                   IEEE International Conference on Web Services, ICWS 2007. IEEE,
              efficient mobile charging for wireless power transfer in internet of                            2007, pp. 304–311.
              things networks,” IEEE Internet of Things Journal, vol. 5, no. 1, pp.                      [50] Y. Achbany, F. Fouss, L. Yen, A. Pirotte, and M. Saerens, “Optimal
              79–92, 2018.                                                                                    tuning of continual online exploration in reinforcement learning,” in
         [30] A. Lakhdari, A. Bouguettaya, and A. G. Neiat, “Crowdsourcing en-                                International Conference on Artificial Neural Networks. Springer,
              ergy as a service,” in International Conference on Service-Oriented                             2006, pp. 790–800.
              Computing. Springer, 2018, pp. 342–351.                                                    [51] H. Wang and P. Tang, “Preference-aware web service composition
         [31] Y. Tong, Z. Zhou, Y. Zeng, L. Chen, and C. Shahabi, “Spatial                                    by reinforcement learning,” in 20th IEEE International Conference
              crowdsourcing: a survey,” The VLDB Journal, vol. 29, no. 1, pp.                                 on Tools with Artificial Intelligence. ICTAI’08., vol. 2. IEEE, 2008,
              217–250, 2020.                                                                                  pp. 379–386.
                                                                                                         [52] A. Moustafa and M. Zhang, “Multi-objective service composition us-
         [32] D. Shin, S. M. Arisona, S. Georgakopoulou, G. Schmitt, and S. Kim,
                                                                                                              ing reinforcement learning,” in International Conference on Service-
              “A crowdsourcing urban simulation platform on smartphone technol-
                                                                                                              Oriented Computing. Springer, 2013, pp. 298–312.
              ogy: Strategies for urban data visualization and transportation mode
                                                                                                         [53] H. Wang, Q. Wu, X. Chen, Q. Yu, Z. Zheng, and A. Bouguettaya,
              detection,” in Proceedings of the 30th eCAADe Conference, 2012,
                                                                                                              “Adaptive and dynamic service composition via multi-agent rein-
              pp. 377–384.
                                                                                                              forcement learning,” in 2014 IEEE International Conference on Web
         [33] G. Marzano, J. Lizut, and L. O. Siguencia, “Crowdsourcing solutions                             Services (ICWS). IEEE, 2014, pp. 447–454.
              for supporting urban mobility,” Procedia Computer Science, vol. 149,                       [54] M. R. Vieira, P. Bakalov, and V. J. Tsotras, “On-line discovery
              pp. 542–547, 2019.                                                                              of flock patterns in spatio-temporal data,” in Proceedings of the
         [34] Y. Chon, N. D. Lane, F. Li, H. Cha, and F. Zhao, “Automatically                                 17th ACM SIGSPATIAL International Conference on Advances in
              characterizing places with opportunistic crowdsensing using smart-                              Geographic Information Systems. ACM, 2009, pp. 286–295.
              phones,” in Proceedings of the 2012 ACM Conference on Ubiquitous                           [55] P. Kalnis, N. Mamoulis, and S. Bakiras, “On discovering moving
              Computing. ACM, 2012, pp. 481–490.                                                              clusters in spatio-temporal data,” in International Symposium on
         [35] M. F. Bulut, Y. S. Yilmaz, and M. Demirbas, “Crowdsourcing                                      Spatial and Temporal Databases. Springer, 2005, pp. 364–381.
              location-based queries,” in 2011 IEEE International Conference on                          [56] M. Ester, H.-P. Kriegel, J. Sander, X. Xu et al., “A density-based
              Pervasive Computing and Communications Workshops (PERCOM                                        algorithm for discovering clusters in large spatial databases with
              Workshops). IEEE, 2011, pp. 513–518.                                                            noise.” in Kdd, vol. 96, no. 34, 1996, pp. 226–231.
         [36] J. Zimmerman, A. Tomasic, C. Garrod, D. Yoo, C. Hiruncharoenvate,                          [57] D. Zhao, H. Wang, H. Ma, H. Xu, L. Liu, and P. Zhang, “Crowdolr:
              R. Aziz, N. R. Thiruvengadam, Y. Huang, and A. Steinfeld, “Field                                Toward object location recognition with crowdsourced fingerprints
              trial of tiramisu: crowd-sourcing bus arrival times to spur co-design,”                         using smartphones,” IEEE Transactions on Human-Machine Sys-
              in Proceedings of the SIGCHI Conference on Human Factors in                                     tems, vol. 47, no. 6, pp. 1005–1016, 2017.
              Computing Systems. ACM, 2011, pp. 1677–1686.                                               [58] H. Wang, D. Zhao, H. Ma, and L. Ding, “Min-max planning of time-
         [37] A. Steinfeld, J. Zimmerman, A. Tomasic, D. Yoo, and R. Aziz,                                    sensitive and heterogeneous tasks in mobile crowd sensing,” in 2018
              “Mobile transit information from universal design and crowdsourc-                               IEEE Global Communications Conference (GLOBECOM). IEEE,
              ing,” Transportation Research Record: Journal of the Transportation                             2018, pp. 1–7.
              Research Board, no. 2217, pp. 95–102, 2011.                                                [59] M. C. Bliemer, M. Dicke-Ogenia, and D. Ettema, “Rewarding
         [38] B. Ferris, K. Watkins, and A. Borning, “Onebusaway: results from                                for avoiding the peak period: a synthesis of four studies in the
              providing real-time arrival information for public transit,” in Pro-                            netherlands,” 2010.
              ceedings of the Conference on Human Factors in Computing Systems                           [60] P. Cohen, R. Hahn, J. Hall, S. Levitt, and R. Metcalfe, “Using
              (SIGCHI). ACM, 2010, pp. 1807–1816.                                                             big data to estimate consumer surplus: The case of uber,” National
         [39] A. B. Said, A. Erradi, A. Ghari Neiat, and A. Bouguettaya, “Mobile                              Bureau of Economic Research, Tech. Rep., 2016.
              crowdsourced sensors selection for journey services,” in Interna-                          [61] C. E. Shannon, “A mathematical theory of communication,” ACM
              tional Conference on Service-Oriented Computing. Springer, 2018,                                SIGMOBILE Mobile Computing and Communications Review,
              pp. 463–477.                                                                                    vol. 5, no. 1, pp. 3–55, 2001.
         [40] B. Kantarci and H. T. Mouftah, “Sensing services in cloud-centric                          [62] İ. K. Altınel, N. Aras, E. Güney, and C. Ersoy, “Binary integer
              internet of things: A survey, taxonomy and challenges,” in 2015 IEEE                            programming formulation and heuristics for differentiated coverage
              International Conference on Communication Workshop (ICCW).                                      in heterogeneous sensor networks,” Computer Networks, vol. 52,
              IEEE, 2015, pp. 1865–1870.                                                                      no. 12, pp. 2419–2431, 2008.
         [41] A. Murturi, B. Kantarci, and S. F. Oktug, “A reference model                               [63] L.-A. Tang, Y. Zheng, J. Yuan, J. Han, A. Leung, C.-C. Hung, and
              for crowdsourcing as a service,” in 2015 IEEE 4th International                                 W.-C. Peng, “On discovery of traveling companions from streaming
              Conference on Cloud Networking. IEEE, 2015, pp. 64–66.                                          trajectories,” in 2012 IEEE 28th International Conference Data
                                                                                                              Engineering (ICDE) on. IEEE, 2012, pp. 186–197.
         [42] G. Iosifidis, L. Gao, J. Huang, and L. Tassiulas, “Enabling crowd-
                                                                                                         [64] E. Naserian, X. Wang, X. Xu, and Y. Dong, “A framework of loose
              sourced mobile internet access,” in IEEE International Conference
                                                                                                              travelling companion discovery from human trajectories,” IEEE
              on Computer Communications INFOCOM, 2014, pp. 451–459.
                                                                                                              Transactions on Mobile Computing, vol. 17, no. 11, pp. 2497–2511,
         [43] X. Sheng, X. Xiao, J. Tang, and G. Xue, “Sensing as a service: A                                2018.
              cloud computing system for mobile phone sensing,” in Sensors 2012.
              IEEE, 2012, pp. 1–4.
         [44] X. Sheng, J. Tang, X. Xiao, and G. Xue, “Sensing as a service:
              Challenges, solutions and future directions,” IEEE Sensors Journal,
              vol. 13, no. 10, pp. 3733–3741, 2013.
         [45] X. Peng, J. Gu, T. H. Tan, J. Sun, Y. Yu, B. Nuseibeh, and
              W. Zhao, “Crowdservice: Serving the individuals through mobile
              crowdsourcing and service composition,” in 2016 31st IEEE/ACM
              International Conference on Automated Software Engineering (ASE).
              IEEE, 2016, pp. 214–219.
         [46] H. Wang and X. Wang, “A novel approach to large-scale services
              composition,” in Asia-Pacific Web Conference. Springer, 2013, pp.
              220–227.
         [47] W. Xu, J. Cao, H. Zhao, and L. Wang, “A multi-agent learning
              model for service composition,” in 2012 IEEE Asia-Pacific Services
              Computing Conference (APSCC). IEEE, 2012, pp. 70–75.


1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/TSC.2021.3064329, IEEE
                                                                                             Transactions on Services Computing

         IEEE TRANSACTIONS ON SERVICES COMPUTING                                                                                                                                                  14



                                 Azadeh Ghari Neiat is a lecturer in the
                                 School of Information Technology at the
                                 Deakin University. Before joining Deakin Uni-
                                 versity, she was a postdoctoral research fel-
                                 low at the University of Sydney since 2017.
                                 She was awarded a PhD in computer science
                                 at RMIT University, Australia in 2017. She
                                 has published in top journals and confer-
                                 ences such as CACM, IEEE TKDE, IEEE
                                 TSC, ACM TOIT, Future Generation Com-
                                 puter Systems, ICSOC, ICWS, MobiQuitous
         etc. Her research interest lies at the intersections of Mobile Crowd-
         sourcing, AI, IoT, and Spatio-Temporal Data Analysis.




                                Athman Bouguettaya is Professor and
                                Head of School of Computer Science at the
                                University of Sydney, Sydney, Australia.He
                                received his PhD in Computer Science from
                                the University of Colorado at Boulder (USA)
                                in 1992. He is or has been on the edito-
                                rial boards of several journals including, the
                                IEEE Transactions on Services Computing,
                                ACM Transactions on Internet Technology,
                                the International Journal on Next Generation
                                Computing, VLDB Journal, Distributed and
         Parallel Databases Journal, and the International Journal of Cooper-
         ative Information Systems. He has published more than 200 books,
         book chapters, and articles in journals and conferences in the area
         of databases and service computing. He is a Fellow of the IEEE and
         a Distinguished Scientist of the ACM.




                                        Mohammed Bahutair is a PhD student in
                                        the School of Computer Science at the Uni-
                                        versity of Sydney, Australia. He received his
                                        bachelor degree in Computer Engineering
                                        from Ittihad University, UAE 2012 and his
                                        Masters degree in Computer Engineering
                                        from University of Sharjah, UAE 2015. His
                                        research interests are Machine Learning ,
                                        Trust, IoT and Big Data Mining.




1939-1374 (c) 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
                 Authorized licensed use limited to: Consortium - Algeria (CERIST). Downloaded on May 16,2021 at 10:32:10 UTC from IEEE Xplore. Restrictions apply.
