# BlocksTechnology USB vendor/product IDs

Klipper (and Katapult, its bootloader) let you set the USB `idVendor`/
`idProduct` a board's firmware reports, per build, via `make menuconfig` →
enable "Enable extra low-level configuration options" (`LOW_LEVEL_OPTIONS`)
→ "USB ids" → `USB_VENDOR_ID` / `USB_DEVICE_ID` (`src/Kconfig` in both
projects). Stock builds all report the same pair (Klipper `1d50:614e`,
Katapult `1d50:6177`), which is why device identification in this repo has
so far relied on the `/dev/serial/by-id` symlink name instead (see
`device_profiles.yaml`) - every stock-ID board looks identical on the bus.

This table is the standard set of IDs for BlocksTechnology-specific boards
(starting with AMU), so a board can be identified by `vendor_id`/
`product_id` alone - reliable even if someone changes the USB descriptor
strings that the symlink name (and therefore the regex `match` fallback)
is built from.

## Vendor ID

Keep `0x1d50` (OpenMoko) - the same VID stock Klipper/Katapult already use,
so a Blocks board still reads as "part of the Klipper family". **This VID
is informally, not centrally, shared**: Klipper's own docs credit OpenMoko
for `0x614e`, but there is no single authority enforcing sub-allocations
under `0x1d50` (the pid.codes registry's shared VID is actually a
*different* one, `0x1209` - see below). Collision risk against `0x1d50` is
therefore non-zero, if low. For a permanent, collision-free allocation,
register a real range through <https://pid.codes/howto/> (their shared VID
`0x1209`, free for open-source projects) and migrate this table to it - do
that before this scheme is relied on outside our own fleet.

## Product ID range

**`0xB000`-`0xB0FF`** reserved for BlocksTechnology boards. Checked against
the community `usb.ids` database (`linux-usb.org`, mirrored at
`github.com/gentoo/hwids`) as of 2026-09-23: nothing under `0x1d50` is
registered between `0x6123` and `0xFFFF` except `0x8085` and `0xcc15`, so
this block is clear of every *documented* device - it is not a guarantee
against an undocumented/unregistered use of the same numbers elsewhere.

Layout: firmware PID in `0xB0`**`0`**`0`-`0xB0`**`7`**`F`, the matching
Katapult-bootloader PID for the same board at `+0x80` (`0xB0`**`8`**`0`-
`0xB0FF`) - so `board_pid | 0x80` always finds its own bootloader without a
second lookup table.

| Board | Klipper firmware | Katapult bootloader |
|---|---|---|
| AMU V1| `0xB001` | `0xB081` |
| *(next board)* | `0xB002` | `0xB082` |

To add a board: take the next unused low byte, keep the `+0x80` bootloader
pairing, add a row here, and add/update its entry in `device_profiles.yaml`
(`vendor_id: '0x1d50'`, `product_id: '0xb0xx'`).

## Applying to a board's firmware build

In that board's Klipper `.config` (and its Katapult `.config`, using the
bootloader PID):

```
CONFIG_LOW_LEVEL_OPTIONS=y
CONFIG_USB_VENDOR_ID=0x1d50
CONFIG_USB_DEVICE_ID=0xb001   # this board's PID from the table above
```

## How matching uses the IDs

device_discoveryd reports each serial device's USB vendor/product ID (read
from sysfs for the USB device behind the tty). `DeviceProfile.matches()`
treats a reported ID as final for profiles that set `vendor_id`: a board
still on Klipper's stock `1d50:614e` does **not** match the AMU profile, even
if its USB serial string contains "AMU". Reflash every AMU with its assigned
PID before relying on detection.

The profile's `match` regex is only used when no ID is reported (0): the
legacy `/dev/serial/by-id` scan used while the daemon is unreachable, or a
daemon older than the sysfs ID lookup.
