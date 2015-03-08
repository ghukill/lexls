from mysolr import Solr
import requests


# solr_handle
from solrHandles import solr_handle


# class for lexls Solr doc
class SolrDoc(object):

	class SolrFields(object):
		def __init__(self, retain_id=True, **fields): 
			self.__dict__.update(fields)
			

	# init
	def __init__(self, id):
		self.id = id

		# get stateful, current Solr doc
		query_params = {
			"q":'id:{id}'.format(id=self.id),
			"rows":1
		}

		response = solr_handle.search(**query_params)		
		
		if len(response.documents) > 0:
			self.doc = self.SolrFields(**response.documents[0])
			#store version, remove from doc
			self.version = self.doc._version_ 
			del self.doc._version_
			# finally, set exists to True
			self.exists = True

		else:
			self.doc = self.SolrFields()
			self.doc.id = self.id # automatically set id
			self.exists = False


	# delete doc in Solr
	def delete(self):
		delete_response = solr_handle.delete_by_key(self.id, commit=False)
		return delete_response


	# update doc to Solr
	def update(self):
		update_response = solr_handle.update([self.doc.__dict__], commit=False)
		return update_response


	def commit(self):
		return solr_handle.commit()

	
	def updateFields(self,dict):
		self.doc = self.SolrFields(**dict)
		self.doc.id = self.id #maintain id even if contained in dict

	
	def asDictionary(self):
		return self.doc.__dict__