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


## License

The project is licensed under the GNU GPLv3 license.
