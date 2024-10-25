const { app, BrowserWindow, protocol, net } = require("electron")
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
