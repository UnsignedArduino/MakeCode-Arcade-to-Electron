PACKAGE_JSON_CONTENTS = r"""{
  "name": "<NAME>",
  "version": "<VERSION>",
  "description": "<DESCRIPTION>",
  "main": "src/main.js",
  "author": "<AUTHOR>",
  "devDependencies": {
    "@electron-forge/cli": "^7.5.0",
    "@electron-forge/maker-deb": "^7.5.0",
    "@electron-forge/maker-rpm": "^7.5.0",
    "@electron-forge/maker-squirrel": "^7.5.0",
    "@electron-forge/maker-zip": "^7.5.0",
    "@electron-forge/plugin-auto-unpack-natives": "^7.5.0",
    "@electron-forge/plugin-fuses": "^7.5.0",
    "@electron/fuses": "^1.8.0",
    "electron": "^33.0.2",
    "pxt": "^0.5.1"
  },
  "scripts": {
    "start": "electron-forge start",
    "package": "electron-forge package",
    "make": "electron-forge make"
  },
  "dependencies": {
    "electron-squirrel-startup": "^1.0.1"
  }
}
"""
FORGE_CONFIG_JS_CONTENTS = r"""const { FusesPlugin } = require("@electron-forge/plugin-fuses");
const { FuseV1Options, FuseVersion } = require("@electron/fuses");

module.exports = {
  packagerConfig: {
    icon: "src/icon",
    asar: true,
  },
  rebuildConfig: {},
  makers: [
    {
      name: "@electron-forge/maker-squirrel",
      config: {},
    },
    {
      name: "@electron-forge/maker-zip",
      platforms: ["darwin"],
    },
    {
      name: "@electron-forge/maker-deb",
      config: {},
    },
    {
      name: "@electron-forge/maker-rpm",
      config: {},
    },
  ],
  plugins: [
    {
      name: "@electron-forge/plugin-auto-unpack-natives",
      config: {},
    },
    // Fuses are used to enable/disable various Electron functionality
    // at package time, before code signing the application
    new FusesPlugin({
      version: FuseVersion.V1,
      [FuseV1Options.RunAsNode]: false,
      [FuseV1Options.EnableCookieEncryption]: true,
      [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
      [FuseV1Options.EnableNodeCliInspectArguments]: false,
      [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
      [FuseV1Options.OnlyLoadAppFromAsar]: true,
    }),
  ],
};
"""
SRC___MAIN_JS_CONTENTS = r"""const { app, BrowserWindow, protocol, net } = require("electron")
const path = require("node:path")
const url = require("node:url")

const createWindow = () => {
  const windowScale = 4
  const mainWindow = new BrowserWindow({
    width: 160 * windowScale,
    height: 127 * windowScale,
    autoHideMenuBar: true,
    icon: "src/icon.png"
  })

  mainWindow.loadFile("src/index.html")
  // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow()

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })

  protocol.handle("https", (rq) => {
    const u = new URL(rq.url)
    const lastPart = u.pathname.split("/").reverse()[0]
    const fileMapping = {
      "---simulator": "./fake-net/---simulator.html",
      "sim.css": "./fake-net/sim.css",
      "icons.css": "./fake-net/icons.css",
      "pxtsim.js": "./fake-net/pxtsim.js",
      "sim.js": "./fake-net/sim.js",
      "---simserviceworker": "./fake-net/---simserviceworker.js",
    }
    if (lastPart in fileMapping) {
      const newURL = url.pathToFileURL(path.join(__dirname, fileMapping[lastPart]))
      console.log(`Caught request to ${rq.url}, returning ${newURL}`)
      return net.fetch(newURL.toString(), { bypassCustomProtocolHandlers: true })
    } else {
      return net.fetch(rq, { bypassCustomProtocolHandlers: true })
    }
  })
})

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit()
})
"""
SRC___INDEX_HTML_CONTENTS = r"""<!--index.html-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script type="text/javascript">
        var channelHandlers = {}

        function addSimMessageHandler(channel, handler) {
            channelHandlers[channel] = handler;
        }

        function makeCodeRun(options) {
            var code = "";
            var isReady = false;
            var simState = {}
            var simStateChanged = false
            var started = false;
            var meta = undefined;

            // hide scrollbar
            window.scrollTo(0, 1);
            // init runtime
            initSimState();
            fetchCode();

            // helpers
            function fetchCode() {
                sendReq(options.js, function (c, status) {
                    if (status != 200)
                        return;
                    code = c;
                    // find metadata
                    code.replace(/^\/\/\s+meta=([^\n]+)\n/m, function (m, metasrc) {
                        meta = JSON.parse(metasrc);
                    })
                    // load simulator with correct version
                    document.getElementById("simframe")
                        .setAttribute("src", meta.simUrl + "?hideSimButtons=1&noExtraPadding=1");
                })
            }

            function startSim() {
                if (!code || !isReady || started)
                    return
                setState("run");
                started = true;
                const runMsg = {
                    type: "run",
                    parts: [],
                    code: code,
                    partDefinitions: {},
                    cdnUrl: meta.cdnUrl,
                    version: meta.target,
                    storedState: simState,
                    frameCounter: 1,
                    options: {
                        "theme": "green",
                        "player": ""
                    },
                    id: "green-" + Math.random()
                }
                postMessage(runMsg);
            }

            function stopSim() {
                setState("stopped");
                postMessage({
                    type: "stop"
                });
                started = false;
            }

            window.addEventListener("message", function (ev) {
                var d = ev.data
                if (d.type == "ready") {
                    var loader = document.getElementById("loader");
                    if (loader)
                        loader.remove();
                    isReady = true;
                    startSim();
                } else if (d.type == "simulator") {
                    switch (d.command) {
                        case "restart":
                            stopSim();
                            startSim();
                            break;
                        case "setstate":
                            if (d.stateValue === null)
                                delete simState[d.stateKey];
                            else
                                simState[d.stateKey] = d.stateValue;
                            simStateChanged = true;
                            break;
                    }
                } else if (d.type === "messagepacket" && d.channel) {
                    const handler = channelHandlers[d.channel]
                    if (handler) {
                        try {
                            const buf = d.data;
                            const str = uint8ArrayToString(buf);
                            const data = JSON.parse(str)
                            handler(data);
                        } catch (e) {
                            console.log(`invalid simmessage`)
                            console.log(e)
                        }
                    }
                }
            }, false);

            // helpers
            function uint8ArrayToString(input) {
                let len = input.length;
                let res = ""
                for (let i = 0; i < len; ++i)
                    res += String.fromCharCode(input[i]);
                return res;
            }

            function setState(st) {
                var r = document.getElementById("root");
                if (r)
                    r.setAttribute("data-state", st);
            }

            function postMessage(msg) {
                const frame = document.getElementById("simframe");
                if (frame)
                    frame.contentWindow.postMessage(msg,
                        meta.simUrl);
            }

            function sendReq(url, cb) {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (xhttp.readyState == 4) {
                        cb(xhttp.responseText, xhttp.status)
                    }
                };
                xhttp.open("GET", url, true);
                xhttp.send();
            }

            function initSimState() {
                try {
                    simState = JSON.parse(localStorage["simstate"])
                } catch (e) {
                    simState = {}
                }
                setInterval(function () {
                    if (simStateChanged)
                        localStorage["simstate"] = JSON.stringify(simState)
                    simStateChanged = false
                }, 200)
            }
        }
    </script>
    <style>
        body {
            background: black;
            color: white;
            font-family: monospace;
            overflow: hidden;
            font-size: 14pt;
        }

        iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
    <title><NAME> <VERSION></title>
</head>
<body id="root">
<iframe id="simframe" allowfullscreen="allowfullscreen"
        sandbox="allow-popups allow-forms allow-scripts allow-same-origin"></iframe>
<script type="text/javascript">
    makeCodeRun({js: "./binary.js"})
</script>
</body>
</html>
"""
