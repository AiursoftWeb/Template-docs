# Global Settings

The Global Settings feature allows you to manage application configuration dynamically without redeploying the application. It supports a hierarchical configuration system effectively combining static configuration (like `appsettings.json` or Environment Variables) with dynamic database-stored settings.

## Configuration Priority

The application resolves settings values in the following order of priority:

1.  **Configuration (Environment Variables / AppSettings)**:
    If a key is present in `appsettings.json` or set as an Environment Variable, this value takes precedence.
    *   Format: `GlobalSettings:Key`.
    *   *Note: If a setting is found here, it becomes read-only in the database UI to prevent confusion.*

2.  **Database**:
    If not found in the configuration, the application checks the database for a stored value. This value is editable via the Admin Dashboard.

3.  **Default Value**:
    If neither of the above exists, the default value defined in the code (`SettingsMap`) is used.

## Managing Settings

Administrators can manage these settings through the **Global Settings** page in the Admin Dashboard.

### Supported Setting Types

The system supports various types of settings with appropriate UI validation:

*   **Text**: Simple string values.
*   **Bool**: Boolean values (True/False switch).
*   **Number**: Numeric values (Integer/Double).
*   **Choice**: A dropdown selection from predefined options.
*   **File**: Allows uploading a file (e.g., for replacing the logo or banner).

## Developer Guide

### Defining New Settings

To add a new global setting, add a new definition in `Aiursoft.Template.Configuration.SettingsMap` class:

```csharp
new GlobalSettingDefinition
{
    Key = "NewFeatureEnabled",
    Name = "Enable New Feature",
    Description = "Whether to enable the new experimental feature.",
    Type = SettingType.Bool,
    DefaultValue = "False"
}
```

### Accessing Settings

Inject the `GlobalSettingsService` to access settings in your services or controllers:

```csharp
public class MyService(GlobalSettingsService settingsService)
{
    public async Task DoWorkAsync()
    {
        // Get raw string value
        var brandName = await settingsService.GetSettingValueAsync("BrandName");

        // Get typed value
        if (await settingsService.GetBoolSettingAsync("NewFeatureEnabled"))
        {
            // Feature logic...
        }
    }
}
```

### Configuration Overrides

To override a setting in production (e.g., using Docker or Kubernetes), simply set an environment variable:

```bash
# Overrides the 'BrandName' setting
GLOBALSETTINGS__BRANDNAME="My Custom Brand"
```
