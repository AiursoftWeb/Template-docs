# Aiursoft Template Tutorial - Step 7 - Add a New Configuration Item and Support Environment Variables

![configuration](./assets/configuration.png)

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

```json title="禁止注册的 appsettings.json"
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
cd ./src/MyOrg.MarkToHtml
AppSettings__Local__AllowRegister=false dotnet run
```

!!! tip "Note the naming convention for environment variables"

    Use double underscores `__` in environment variables to represent the hierarchy of configuration items. For example, `AppSettings:Local:AllowRegister` is represented as `AppSettings__Local__AllowRegister` in environment variables.

You will also notice that the register button has disappeared.

In actual production scenarios, we recommend using environment variables for configuration, as this makes it easier to version control our configuration information.

## Step 7.2 - Add a New Configuration Item

In the previous example, we demonstrated a configuration item `AppSettings:Local:AllowRegister` that is already supported by the application. But what if we need to add a completely new configuration item?

Below, we will use `AppSettings:AllowAnonymousUsage` as an example to demonstrate how to add a new configuration item and use it in the code.

First, edit the `AppSettings` section in the `appsettings.json` file, and add a new configuration item `AllowAnonymousUsage`, setting its default value to `true`:

```json title="添加新的配置项 AllowAnonymousUsage"
...
  "AppSettings": {
    "AuthProvider": "Local",
    "DefaultRole": "",
    "PersistsSignIn": false,
    "AllowAnonymousUsage": true, // 新增的配置项
    ...
  }
...
```

Next, we edit the `./src/MyOrg.MarkToHtml/Configuration/AppSettings.cs` file and add a new property `AllowAnonymousUsage`:

```csharp title="添加新的配置项 AllowAnonymousUsage"
public bool AllowAnonymousUsage { get; init; } = true;
```

At this point, the `AppSettings.cs` file might look like the following:

```csharp title="AppSettings.cs 完整代码"
namespace MyOrg.MarkToHtml.Configuration;

public class AppSettings
{
    public required string AuthProvider { get; init; } = "Local";
    public bool LocalEnabled => AuthProvider == "Local";
    public bool OIDCEnabled => AuthProvider == "OIDC";

    public required OidcSettings OIDC { get; init; }
    public required LocalSettings Local { get; init; }

    /// <summary>
    /// Keep the user sign in after the browser is closed.
    /// </summary>
    public bool PersistsSignIn { get; init; }

    /// <summary>
    /// Automatically assign the user to this role when they log in.
    /// </summary>
    public string? DefaultRole { get; init; } = string.Empty;

    /// <summary>
    /// Allow anonymous users to use the application.
    /// </summary>
    public bool AllowAnonymousUsage { get; init; } = true; // <-- 新增的配置项
}
```

Next, we can use this new configuration option in the code.

The purpose of this configuration option is to disable anonymous usage. We directly go to the `./src/MyOrg.MarkToHtml/Controllers/HomeController.cs` file and first request `IOptions<AppSettings>` from dependency injection:

```csharp title="在 HomeController 中注入 IOptions<AppSettings>"
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

```csharp title="在 Index 方法中检查 AllowAnonymousUsage 配置项"
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

Similarly, the POST method of `Index` also needs to check this configuration item. Eventually, the `HomeController.cs` file might look like this:

```csharp title="HomeController.cs 完整代码"
using System.ComponentModel.DataAnnotations;
using Aiursoft.CSTools.Tools;
using MyOrg.MarkToHtml.Models.HomeViewModels;
using MyOrg.MarkToHtml.Services;
using Aiursoft.UiStack.Navigation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using MyOrg.MarkToHtml.Configuration;
using MyOrg.MarkToHtml.Entities;

namespace MyOrg.MarkToHtml.Controllers;

public class HomeController(
    IOptions<AppSettings> appSettings,
    ILogger<HomeController> logger,
    UserManager<User> userManager,
    TemplateDbContext context,
    MarkToHtmlService mtohService) : Controller
{
    [RenderInNavBar(
        NavGroupName = "Features",
        NavGroupOrder = 1,
        CascadedLinksGroupName = "Home",
        CascadedLinksIcon = "home",
        CascadedLinksOrder = 1,
        LinkText = "Convert Document",
        LinkOrder = 1)]
    public IActionResult Index()
    {
        if (!User.Identity!.IsAuthenticated && !appSettings.Value.AllowAnonymousUsage)
        {
            logger.LogWarning("Anonymous user trying to access the home page. But it is not allowed.");
            return Challenge();

        }
        return this.StackView(new IndexViewModel());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Index(IndexViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return this.StackView(model);
        }

        var userId = userManager.GetUserId(User);
        if (User.Identity?.IsAuthenticated == true && !string.IsNullOrWhiteSpace(userId))
        {
            // If the user is authenticated, this action only saves the document in the database. And it's `edit` action to render it.
            // And go to the edit page.
            logger.LogTrace("Authenticated user submitted a document with ID: '{Id}'. Save it to the database.",
                model.DocumentId);
            var documentInDb = await context.MarkdownDocuments
                .FirstOrDefaultAsync(d => d.Id == model.DocumentId && d.UserId == userId);
            if (documentInDb != null)
            {
                logger.LogInformation("Updating the document with ID: '{Id}'.", model.DocumentId);
                documentInDb.Content = model.InputMarkdown.SafeSubstring(65535);
                documentInDb.Title = model.Title;
            }
            else
            {
                logger.LogInformation("Creating a new document with ID: '{Id}'.", model.DocumentId);
                model.DocumentId = Guid.NewGuid();
                var newDocument = new MarkdownDocument
                {
                    Id = model.DocumentId,
                    Content = model.InputMarkdown.SafeSubstring(65535),
                    Title = model.InputMarkdown.SafeSubstring(40),
                    UserId = userId
                };
                context.MarkdownDocuments.Add(newDocument);
            }

            await context.SaveChangesAsync();
            return RedirectToAction(nameof(Edit), new { id = model.DocumentId });
        }
        else
        {
            if (!appSettings.Value.AllowAnonymousUsage)
            {
                logger.LogWarning("Anonymous user submitted a document with ID: '{Id}'.", model.DocumentId);
                return Challenge();
            }

            // If the user is not authenticated, just show the result.
            logger.LogInformation(
                "An anonymous user submitted a document with ID: '{Id}'. It was not saved to the database.",
                model.DocumentId);
            model.OutputHtml = mtohService.ConvertMarkdownToHtml(model.InputMarkdown);
            return this.StackView(model);
        }
    }

    
    ... other methods ...
```

Other methods of HomeController are omitted. These methods are accessible only to logged-in users and are already protected using the `[Authorize]` attribute. No additional configuration checks are needed from us.

## Step 7.3 - Test the New Configuration Item

Next, we can test this new configuration item. Use the following command to start the project:

```bash title="使用新的配置项启动项目"
cd ./src/MyOrg.MarkToHtml
AppSettings__AllowAnonymousUsage=false dotnet run
```

Then open the browser and visit `http://localhost:5000`. We will notice that if we log out the current user, the home page can no longer be accessed, and the application will automatically redirect to the login page.

## Conclusion

That concludes the seventh step of the Aiursoft Template tutorial. In this step, we learned how to add a new configuration item and use it in the code to change the application's behavior.

We also learned about the ASP.NET Core configuration system and how to use the `appsettings.json` file and environment variables to configure the application.

This will lay a solid foundation for deploying the application in `Docker` in the future, as well as for flexible configuration in production environments.
