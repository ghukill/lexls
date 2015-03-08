# process

#python modules
import csv
import md5
import locale
import logging


# local modules
import models


dictionaries = [	
	{
	  "name":"All Words - 20,000",
		"filename":"all_words_academic_count.csv",
		"target_fields":["sp","ac"]
	},
	# {
	# 	"name":"Small Test",
	# 	"filename":"small_test.csv",
	# 	"target_fields":["sp","ac"]
	# }
]


def processDictionaries(verbose=False):
	
	for dictionary in dictionaries:
		
		logging.info("Working on: {name}".format(name=dictionary['name']))

		with open(dictionary['filename'], 'rb') as csvfile:
			rows = csv.reader(csvfile, delimiter=',')
			rows.next()
			count = 0
			for row in rows:
				logging.debug(row)
				
				id = md5.new(row[0]).hexdigest()

				try:

					# field_dict = {
					# 	"id" : id,
					# 	dictionary['target_field'] : row[0].encode('utf-8'),
					# 	"rank_i" : row[1].replace(",","")
					# }
					
					field_dict = {
						"id" : id,
						"rank_i" : row[1].replace(",","")
					}

					# add target solr fields
					for field in dictionary['target_fields']:
						field_dict[field] = row[0].encode('utf-8')					

					logging.debug(field_dict)

					# open lexlsDoc
					lexlsDoc = models.SolrDoc(id)
					lexlsDoc.updateFields(field_dict)

					# index
					logging.debug(lexlsDoc.update())
				except:
					logging.warning("Could not index string: {payload}".format(payload=str(row)))

				# bump counter, update every 500
				count += 1
				if count % 100 == 0:
					logging.info("{num} completed...".format(num=count))

			logging.info("Finished with: {name}".format(name=dictionary['name']))

		
		# commit dictionary
		models.solr_handle.commit()


	logging.info("Complete.")



if __name__ == "__main__":
	
	logging.basicConfig(level=logging.INFO)
	processDictionaries()
