<b>Job Scraper</b>

This is a script that scanned the israeli job posting website Alljobs.co.il
The data is pushed to a local elastic search instance with the index names the same as the search title

#Prerequisits
Elasticsearch URL installed / defined


#Configuration - config.py

"title" - this is the title of the job description that will be matched
"elasticURL" - points to the elatciseatch instance to send the requests to

#run
main.py


#Kibaba

sample dashboard created in Kibana over the elasticsearch instance, to showcase the results


![Alt text](/KibanaDashboard.png?raw=true "Devops")

