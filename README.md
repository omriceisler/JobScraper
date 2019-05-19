<b>Job Scraper</b>

This is a script that scanned the israeli job posting website Alljobs.co.il
The data is pushed to a local elastic search instance with the index names the same as the search title

<b>Prerequisits</b>
Elasticsearch URL installed / defined


<b>Configuration - config.py</b>

"title" - this is the title of the job description that will be matched
"elasticURL" - points to the elatciseatch instance to send the requests to

<b>run</b>
main.py


<b>Kibaba</b>

sample dashboard created in Kibana over the elasticsearch instance, to showcase the results

![Alt text](/KibanaDashboard.png?raw=true "Devops")

