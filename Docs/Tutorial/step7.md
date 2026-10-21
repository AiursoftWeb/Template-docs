# Aiursoft Template Tutorial - Step 7 - Add a New Configuration Item and Support Environment Variables

![configuration](./images/configuration.png)

As a site administrator, there may be some application configurations that the default settings cannot meet. We need to allow administrators to adjust certain configuration items themselves to change the application's default behavior, for example:

* Allow or disallow new user registration.
* Allow or disallow anonymous users from using the application.
* Allow or disallow users from deleting their own content.

## Step 7.1 - Understand the ASP.NET Core Configuration System (Optional)

Aiursoft Template uses the built-in configuration system of ASP.NET Core. The configuration system allows us to load configuration data from multiple sources, such as:

* appsettings.json file
* appsettings.{Environment}.json file, which means appsettings.Development.json in the development environment and appsettings.Production.json in the production environment.
* Environment variables
* Command-line arguments

Typically, we use the `appsettings.json` file for local development configuration.

!!! tip "For Docker users who want to edit configurations easily"

    When deploying in Docker, the `appsettings.json` file will be exposed to the `/data` directory, so we can directly modify this file to change the configuration.

    Therefore, we highly recommend Docker users to mount a host path to the container's `/data` directory during deployment, so that they can directly edit the configuration file on the host to change the configuration inside the container.

!!! warning "Note: You need to restart the application after each configuration file change"

    The ASP.NET Core configuration system does not automatically monitor changes to configuration files, so you must restart the application after modifying the configuration file for the new settings to take effect.

!!! question "Question: Can I include sensitive information in the configuration?"

    Sensitive information such as database connection strings, API keys, etc., is recommended not to be directly written in configuration files, but instead passed via environment variables. This allows for quick regeneration of configurations based on declarative settings during renewal, without worrying about sensitive information leakage.

For example, we can now try to disable the login and registration features of the application.

First, use the first method: open the `./src/MyOrg.MarkToHtml/appsettings.json` file and set its `AppSettings:Local:AllowRegister` field to `false`.

At this point, the JSON might look like this:

```json
{
  "ConnectionStrings": {
    "AllowCache": "True",
    "DbType": "Sqlite",
    "DefaultConnection": "DataSource=app.db;Cache=Shared"
  },
  "Storage": {
    "Path": "/tmp/data"
  },
  "AppSettings": {
    "AuthProvider": "Local", // OIDC or Local
    "DefaultRole": "",
    "PersistsSignIn": false,
    "OIDC": {
      // https://auth.aiursoft.com/application/o/template
      "Authority": "https://auth.aiursoft.com/application/o/template",
      "ClientId": "",
      "ClientSecret": "",
      "RolePropertyName": "groups",
      "UsernamePropertyName": "preferred_username",
      "UserDisplayNamePropertyName": "name",
      "EmailPropertyName": "email",
      "UserIdentityPropertyName": "sub"
    },
    "Local": {
      "AllowRegister": false,
    }
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

After saving the file, restart the application. We will notice that the registration button has disappeared.

Similarly, we can use environment variables to override configurations in the configuration file.

This time, we roll back the configuration in the `appsettings.json` file. Considering that environment variables have higher priority, we can directly set the environment variable `AppSettings__Local__AllowRegister` to `false` to disable the registration feature.

!!! note "Environment variables have the highest priority"

    In the ASP.NET Core configuration system, environment variables take precedence over configurations in configuration files. Therefore, we can use environment variables to override configurations in configuration files.

    In the example above, even if we set `AppSettings:Local:AllowRegister` to `true` in the `appsettings.json` file, as long as we set the environment variable `AppSettings__Local__AllowRegister` to `false`, the registration feature will still be disabled.

    Therefore, in production environments, especially when deploying with Docker, we recommend using environment variables to configure the application instead of directly modifying configuration files.

This time, use the following command to start the project:

```bash
AppSettings__Local__AllowRegister=false dotnet run --project ./src/MyOrg.MarkToHtml/MyOrg.MarkToHtml.csproj
```

!!! tip "Note the naming convention for environment variables"

    Use double underscores `__` in environment variables to represent the hierarchy of configuration items. For example, `AppSettings:Local:AllowRegister` is represented as `AppSettings__Local__AllowRegister` in environment variables.

You will also notice that the register button has disappeared.

In actual production scenarios, we recommend using environment variables for configuration, as this makes it easier to version control our configuration information.

## Step 7.2 - Add a New Configuration Item

In the previous example, we demonstrated a configuration item `AppSettings:Local:AllowRegister` that is already supported by the application. But what if we need to add a completely new configuration item?

Below, we will use `AppSettings:AllowAnonymousUsage` as an example to demonstrate how to add a new configuration item and use it in the code.

First, edit the `AppSettings` section in the `appsettings.json` file, and add a new configuration item `AllowAnonymousUsage`, setting its default value to `true`:

```json
...
  "AppSettings": {
    "AuthProvider": "Local",
    "DefaultRole": "",
    "PersistsSignIn": false,
    "AllowAnonymousUsage": true, // New setting
    ...
  }
...
```

Next, we edit the `./src/MyOrg.MarkToHtml/Configuration/AppSettings.cs` file and add a new property `AllowAnonymousUsage`:

```csharp
public bool AllowAnonymousUsage { get; init; } = true;
```

Preserve the existing AppSettings properties and add only AllowAnonymousUsage.

Next, we can use this new configuration option in the code.

The purpose of this configuration option is to disable anonymous usage. We directly go to the `./src/MyOrg.MarkToHtml/Controllers/HomeController.cs` file and first request `IOptions<AppSettings>` from dependency injection:

```csharp
public class HomeController(
    IOptions<AppSettings> appSettings,
    ILogger<HomeController> logger,
    UserManager<User> userManager,
    TemplateDbContext context,
    MarkToHtmlService mtohService) : Controller
```

Then, in the `Index` method, check this configuration. If the application disables anonymous access and the current user is not logged in, directly return `Challenge()` to force the user to log in:

!!! tip "What is the `Challenge()` method?"

    The `Challenge()` method triggers the authentication middleware, which typically redirects the user to the login page. If you're using OIDC authentication, it redirects the user to the OIDC provider's login page.

    Returning `Challenge()` is far more generic and reliable than `return RedirectToAction("Login", "Account")`. Especially when considering that the application might support multiple authentication methods, such as OIDC, Local, etc.

```csharp
    public IActionResult Index()
    {
        if (!User.Identity!.IsAuthenticated && !appSettings.Value.AllowAnonymousUsage)
        {
            logger.LogWarning("Anonymous user trying to access the home page. But it is not allowed.");
            return Challenge();
        }
        return this.StackView(new IndexViewModel());
    }
```

Similarly, the POST method of `Index` also needs to check this configuration item. Preserve the existing controller and add the anonymous-access check:

In the existing Index POST action, add this at the start of its anonymous `else` branch, before conversion:

```csharp
if (!appSettings.Value.AllowAnonymousUsage)
{
    return Challenge();
}
```

Keep the authenticated save branch, validation, Edit, History and Delete actions from Step 5. Do not replace existing methods with omitted-code placeholders.

Other methods of HomeController are omitted. These methods are accessible only to logged-in users and are already protected using the `[Authorize]` attribute. No additional configuration checks are needed from us.

## Step 7.3 - Test the New Configuration Item

Next, we can test this new configuration item. Use the following command to start the project:

```bash
AppSettings__AllowAnonymousUsage=false dotnet run --project ./src/MyOrg.MarkToHtml/MyOrg.MarkToHtml.csproj
```

Then open the browser and visit `http://localhost:5000`. We will notice that if we log out the current user, the home page can no longer be accessed, and the application will automatically redirect to the login page.

## Conclusion

That concludes the seventh step of the Aiursoft Template tutorial. In this step, we learned how to add a new configuration item and use it in the code to change the application's behavior.

We also learned about the ASP.NET Core configuration system and how to use the `appsettings.json` file and environment variables to configure the application.

This will lay a solid foundation for deploying the application in `Docker` in the future, as well as for flexible configuration in production environments.
