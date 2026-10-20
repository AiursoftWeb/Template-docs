# Aiursoft Template Tutorial - Step 13 - After-Class Exercises

This part is left for you to complete on your own. You can try adding more features. By now, completing the following features should no longer be a challenge for you.

These features will not only greatly enrich your application but also allow you to deeply master professional knowledge in database design, backend architecture, frontend interaction, and performance optimization through hands-on practice. Have fun!

## Step 13.1 Markdown Supports Multiple Privacy Options

Now, after saving Markdown, only you can view it. We can try adding more privacy options, such as:

* Public: Anyone can view this document.
* Private: Only you can view this document.
* Password-protected: Access to this document requires entering a password.
* Shared with specific user groups: Only members of specific user groups can view this document.

Similarly, for public documents that do not belong to you, we also need to build a separate preview page. When others open the link to a public document, they should see a clean preview page.

When users browse their own document list, they should be able to quickly determine whether the documents are public or private. And they should be able to directly copy the shareable link of public documents and send it to others.

For documents shared with specific user groups, only logged-in users who are members of that group can access them. This is a critical enterprise-level document sharing capability.

## Step 13.2 Support for Other Formats

In addition to Markdown, we can support more formats, such as:

* Mermaid: A text-based format for drawing diagrams and flowcharts.
* LaTeX: A markup language used for typesetting mathematical formulas and scientific documents.
* HTML: Directly input HTML code and render it into a webpage.
* Rich Text Format (WYSIWYG): Allows users to create and edit documents using an editor similar to Word.

## Step 13.3 Search

We can try implementing a search feature that allows users to search their documents by title or content. This can be achieved using full-text indexing or simple string matching. Even support for fuzzy search and advanced search options can be added.

## Step 13.4 Document Version History and Rollback

When editing documents, users might accidentally delete important content or want to retrieve a previous version. Implementing a version control system so that each save becomes a traceable historical record.

This requires careful data structure design, for example:

* Save a complete snapshot of the document with each submission. This is easier to implement and supports rollback to any version, but it consumes more storage space.
* Alternatively, only save the differences (diffs) between each change. This saves storage space but is more complex to implement.

## Step 13.5 Advanced Organization: Folders and Tags System

As the number of documents increases, a flat list becomes difficult to manage. Introducing folders and tags helps users organize their documents.

This requires careful design of the database structure, for example:

* Folders table: stores folder information such as name, creation time, user ID, etc.
* Tags table: stores tag information such as name, color, etc.
* Document-Tag association table: implements many-to-many relationship, allowing a document to have multiple tags.
* Document-Folder association: allows a document to belong to one folder.
* User-Folder association: allows users to create and manage their own root folders.

## Step 13.6 Performance Optimization: Paginated Loading

If a user has hundreds or even thousands of documents, loading all documents at once on the "My Documents" page will cause slow page loading and put pressure on the server and database. By using paginated loading, only the documents on the current page are loaded, improving user experience.

This requires adding two parameters `page` and `pageSize` to the list page, and using `Skip` and `Take` methods in database queries to implement pagination. These will be translated into SQL statements using `OFFSET` and `LIMIT`, thus querying only the required data.

## Step 13.7 Support for PostgreSQL

We have already supported SQLite and MySQL. Now we can try adding support for PostgreSQL. PostgreSQL is a powerful and widely used open-source relational database management system. By adding support for PostgreSQL, the application can adapt to more deployment environments and user needs.

In the design of Aiursoft Template, no core code needs to be modified to easily add support for new databases. You only need to mimic the implementations of MySql and Sqlite, create a new PostgreSql support class, and ensure the connection string and database type are correctly set in the configuration file.
