# Flai QGIS plugin

This QGIS plugin provides GUI access to Flai’s Open Lidar Data Hub and local control over the Flai CLI for AI-powered geospatial classification.

The plugin requires QGIS 3.0 or higher.

To see it on the QGIS Plugin Repository, go to: https://plugins.qgis.org/plugins/flai-cli-interface/

The code is also published on the Github repository: https://github.com/flai-ai/flai-cli-interface

We have also published blog post with detailed description for what plugin can be used and know-how: https://www.flai.ai/post/flai-in-qgis-open-data-and-ai-analysis-one-click-away

We look forward to hearing your feedback!


## Installing

"Stable" releases are available through the official QGIS plugins repository.

After installing the plugin, you may need to manually install our SDK with Pip (this should be automatically handled by our plugin).

```bash
pip install flai-sdk
```

You are all set :D


## Using

To run the Flai QGIS plugin, follow these steps:
1. Go to `Plugins > Flai > Show` to open the plugin.
2. You will see the `DataHub`, `Processing Engine` and `Settings` tabs. On the `DataHub` tab, you can access open LiDAR data. On the `Processing Engine` tab, you can use our paid solution to process point clouds, rasters and vectors. Lastly, the `Settings` tab contains all the controls and settings related to our plugin. For more information and a demonstration of the plugin's functionality, please see our [blog](https://www.flai.ai/post/flai-in-qgis-open-data-and-ai-analysis-one-click-away) (mentioned above).
3. Have fun!


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


### How can I manually update FLAI-SDK package?

Call for manually installing be found here: https://github.com/flai-ai/flai-sdk

#### Windows

Search for `OSGeo4W Shell` and open it. Then call pip install command from link above.

#### Linux

Depending on Python and QGIS install you can install it through system python (not recommended) or with Mamba / Conda.

#### MacOS

Depending on QGIS verison installed (LTS or rolling release) you can install it with `/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3 -m pip` or `/Applications/QGIS.app/Contents/MacOS/bin/python3 -m pip`.


### Where can I locate installed plugin(s)?

#### Windows

Should be on this location: `%AppData%\Roaming\QGIS\QGIS3\profiles\default\python\plugins`

#### Linux

On this location (even if installed through Mamba or Native system installer): `/home/$USER/.local/share/QGIS/QGIS3/profiles/default/python/plugins`


#### MacOS

Should be on this location: `$HOME/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins`


### How do I install QGIS with Mamba / Conda on Linux?

This installation may be compatible with other operating systems, too. Mamba is used in this example because it is less bloated than Conda, and working with it is a breeze.

```bash
# download installer
curl -L -O \
  https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh

# run installer
bash Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3

# init miniforge3 for current shell (in this example zsh - just change name to bash, fish)
$HOME/miniforge3/bin/mamba shell init --shell zsh --root-prefix=~/.local/share/mamba

zsh # to get update script for our shell
mamba create -n py-gis qgis=3.28.9 python=3.9 # choose desired QGIS version here

# call virt enviorment
mamba activate py-gis

# launch QGIS
qgis
```


## License

The project is licensed under the GNU GPLv3 license.
