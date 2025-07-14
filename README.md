# Flai CLI interface

This plugin gives you user-friendly control over the Flai CLI, providing access to advanced FLAI solutions while allowing you to use your own hardware to process data.

The plugin requires QGIS 3.0 or higher.

To see it on the QGIS Plugin Repository, go to: https://plugins.qgis.org/plugins/flai-cli-interface/

The code is also published on the Github repository: https://github.com/flai-ai/flai-cli-interface

We look forward to hearing your feedback!


## Installing

"Stable" releases are available through the official QGIS plugins repository.

After installing the plugin, you may need to manually install our SDK with Pip (this should be automatically handled by our plugin).

```bash
pip install flai-sdk
```

You are all set :D


## Using

To run the Flai CLI interface, follow these steps:
1. Go to `Plugins > Flai CLI > Show` to open the plugin.
2. Fill out the information on the `Getting started` tab. Once you have successfully selected the `Flai CLI` part of the GUI, parts of `Getting started` tab will become disabled and the `Processing tab` will unlock. You can also access the `DataHub` tab without selecting Flai CLI (in development).
3. To `run a flow` on the `Processing tab` using Flai CLI, `select the flow and fill out` the missing information. Once you are happy with the configured flow, you can `check its status` under the `Logs` tab on the `Processing` tab. While processing is happening, parts of the GUI on the `Processing tab` will be disabled. If `something goes` wrong, click the `Reset` button on the `Getting Started` tab. There is also a `Hard Reset` button if the `Reset` button cannot recover our plugin. It can be found by going to `Plugins > Flai CLI > Hard Reset`.
4. Have fun!


## Known issues and limitations

### I think something is wrong with settings file. Where can i find it and edit it?

Our setting file is called `.settings.ini` file and it can be found in plugin's folder. If you decide to deleting whole file, QGIS needs to be closed otherwise some variables can be remembered from before. Below will be commands which will open it in a editor on your system. 

- Windows: 
  - CMD: `notepad %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\flai_cli_interface\.settings.ini`
  - Powershell: `notepad $HOME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\flai_cli_interface\.settings.ini`
    
- Linux:
   - Gnome (Ubuntu): `gnome-text-editor $HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/flai-cli-interface/.settings.ini`
   - KDE: `kate $HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/flai-cli-interface/.settings.ini`
   - VS Code: `code $HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/flai-cli-interface/.settings.ini`
     
   - Terminal based editors:
     - Nano: `nano $HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/flai-cli-interface/.settings.ini`
     - Vim: `vim $HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/flai-cli-interface/.settings.ini`


## License

The project is licensed under the GNU GPLv3 license.
