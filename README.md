# Reffer

This is supposed to be a community based bibliography management solution. The idea is that people can upload their bib files which will be stored in a database. And people can also search by different fields. The application is fairly straightforward and self-explanatory so it is almost pointless to explain the features in any more details right now.

## Database and Storage Limitation

Naturally, the project is not hosted in a premiem tier database. In fact, it is hosted on a free tier [Couchbase Capella](https://www.couchbase.com/products/capella/) platform. This allows a NoSQL database of 8GB (SQL++, actually). And it will remain this way so 8GB is the hard limit. After that I guess the application will not be adding any new bibliographic entry. Please keep that in mind when you use this application and be as reasonable as possible. I will try to place some filters when adding new entries to avoid having duplicates as much as possible. Use the search feature first to see if the entry you are looking for already exists in the database or not.
