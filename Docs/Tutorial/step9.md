# Aiursoft Template Tutorial - Step 9 - Allow Users to Upload Files from the Frontend

Use the existing file storage services to accept uploads, save their relative paths in your models, and generate public URLs when rendering views. Follow the [File Upload guide](../Features/SaveFile.md) for the controller, storage, and view examples.

Keep the upload endpoint protected by the appropriate permission and validate the uploaded file before saving it. Store the relative path rather than a server filesystem path or a hard-coded public URL.

Continue with [Step 10 - Soft Delete and Recycle Bin](./step10.md).
