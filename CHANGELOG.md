# Change Log

## Next release

### 🔧 Fixed

* Fix the `/sync_to_zenith` endpoint. Remove the unpark and park commands which were causing the telescope to move during syncing.

### ⚙️ Engineering

* Use `ty` for type checking and update dependencies in uv lockfile.
* Add `lint` workflow.


## 0.1.0 - 2026-07-11

### 🔥 New

* Initial release with support for ASCII and ASCOM server (although only the former is properly tested). The `/ascii` route supports the following commands:
  * `/status` - Returns the telescope status and position.
  * `/sync_to_zenith` - Synchronizes the telescope to the zenith.
  * `/park` - Parks the telescope at zenith.
  * `/goto_cover` - Goes to the cover position.
  * `/stop` - Stops the telescope movement.
