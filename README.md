# exploring-ltns
An experiment to derive Low Traffic Neighbourhood boundaries from routing data.

# What's all this about?

***This is a personal side project. Part of my motivation is to improve my understanding of the publically available data and the technology, in addition to exploring local policy quesitons.***

There are few aspects of modern life that have not been affected by Covid-19. Like many city's, Newcastle City Council introduced a number of changes with the intention of supporting social distancing. In the suburb of Gosforth (where I live), this included closing a number of roads to through motor traffic, establishing "Low Traffic Neighbourhoods" (LTNs).

A local campaining group "Space for Gosforth", wrote [this blog article](http://spaceforgosforth.com/bollards) which pointed out that these measures are not new and there are already a number of local areas which are closed to through motor traffic, even if they weren't called LTNs origionally.

The blog article included a map showing the new and previously-established LTNs. This appeared to have been drawn based on local-knowledge. Whilst I do not dispute the validity of their map, I am curious to know whether or not these areas could be devired from existing data without the need to *rely* on local expertise.

# Aims

This repo aims to tackle the question "Can the claim (that LTNs are merely a new name for an established planning practise) be supported by existing data, without replying on (subjective, if expert) local knowledge?

# Objectives

* **Reproducible** - Another person (with suitable knowldeg of the tools involved) could re-run the experiment and get the same result.
* **Transferable** - The methodology should not limited to a single geography. It should be easily transferable to another UK city, where equivilant data exists.

* **Parameterisable** - It should be easy for a user to adjust any parameters which are important for the model.

* **Openly licenced** - This means that:
  * The model itself should be openly licenced.
  * It should only depend on openly licenced, publically available data.
  * It should only use open source software.

# Area of Interest

Given the objective of being transferable, the precise area of interest in somewhat arbitary,

For development purposes I have limited myself to to the council wards which include the LTNs in the Space for Gosforth blog. Which is roughly the area bounded by, the Town Moor to the south, the A1 to the West, the Race Course to the north and boundary with North Tyneside to the north-east and cuts through parts of Heaton and Jesmond to the south-east. With the exception of the south-east, this generally conicides with some existing boundaries in the geography of the city.
