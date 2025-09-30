# 📜 ATTRIBUTIONS

BlocksScreen is built upon the work of several outstanding open-source projects. This file documents all derivative code, acknowledgments, and licensing considerations to ensure full transparency and compliance.

---

## 🧩 Upstream Projects

### 1. KlipperScreen  
- **Repository**: [https://github.com/KlipperScreen/KlipperScreen](https://github.com/KlipperScreen/KlipperScreen)  
- **License**: GNU Affero General Public License v3.0 (AGPL-3.0)  
- **Usage**:  
  - Portions of the UI logic, layout structure were adapted and modified.  
  - Specific methods and class structures were reworked to fit the BlocksScreen architecture.  
- **Modifications**:  
  - Refactored for PyQt6 compatibility  
  - Rewritten input handling and display logic for BLOCKS hardware  

---

### 2. Moonraker  
- **Repository**: [https://github.com/arksine/moonraker](https://github.com/arksine/moonraker)  
- **License**: GNU Affero General Public License v3.0 (AGPL-3.0)  
- **Usage**:  
  - BlocksScreen communicates with Moonraker via its HTTP API.  
  - API schemas and endpoint logic were referenced to build the GUI’s backend.  
- **Modifications**:  
  - Custom API wrappers for BLOCKS-specific printer states  
  - Enhanced error handling and async integration with PyQt event loop

---

### 3. Klipper Firmware  
- **Repository**: [https://github.com/Klipper3d/klipper](https://github.com/Klipper3d/klipper)  
- **License**: GNU General Public License v3.0 (GPL-3.0)  
- **Usage**:  
  - BlocksScreen indirectly interfaces with Klipper via Moonraker.  
  - No direct code from Klipper is included, but its configuration and status models informed GUI design.

---

## 🚫 No Affiliation Disclaimer

BlocksScreen is independently developed and maintained. It is **not affiliated with or endorsed by** the maintainers of KlipperScreen, Moonraker, or Klipper Firmware.

---

## 📘 Licensing Notes

- All derivative code complies with the AGPL-3.0 license.  
- This project preserves original copyright notices where applicable.  
- Any redistributed or modified versions of BlocksScreen must also comply with AGPL-3.0 and retain this attribution file.

---

## 🛠 Additional Tools & Libraries

If you’ve used other third-party libraries (e.g. `requests`, `PyQt6`, `aiohttp`, etc.), you can add a section like:

```markdown
### PyQt6  
- **License**: GPL v3  
- **Usage**: Core GUI framework  
- **Repository**: [https://www.riverbankcomputing.com/software/pyqt/intro](https://www.riverbankcomputing.com/software/pyqt/intro)



