# BB10 Blue LED Recovery

[简体中文](README.md) | English

This project preserves and documents **BlackBerryFix**, a historical utility for a BlackBerry 10 issue in which some devices lose data after a restart and show a blue notification LED during startup. It contains the tool, file hashes, and a record of a real repair attempt.

**This is an independent preservation project, not an official BlackBerry project or a VoLTE activation tool.** A blue LED does not prove a particular diagnosis, and a success message alone does not prove that data will persist.

## The problem

The historical BlackBerry knowledge-base article KB36747 described devices deleting data on manual restart and displaying a blue LED while booting. Our Q10 repeatedly lost applications, settings, and newly written test files after normal restarts, with a blue light during boot. The issue remained after a full OS reflash.

This project cannot restore data already lost or guarantee a fix for every device or blue-LED problem.

## Downloads

| File | Purpose and status |
| --- | --- |
| [BlackBerryFix.exe](vendor/windows/BlackBerryFix.exe) | Windows repair utility, run on the Q10 described below; **no Authenticode signature**. |
| [BlackBerryFix.zip](vendor/windows/BlackBerryFix.zip) | Original Windows archive containing that executable. |
| [KB36747_BlackBerryFixMac.zip](vendor/mac/KB36747_BlackBerryFixMac.zip) | Historical Mac version, **not tested by this project**. Its program is 32-bit x86; [macOS Catalina 10.15 and later do not support 32-bit apps](https://support.apple.com/en-us/103076). |

Use the GitHub download button on a file page or clone the repository. The original program's source code and license were not included in the archives; see [License and attribution](#license-and-attribution).

## Windows procedure

1. **Back up important data somewhere outside the phone first.** Repair may cause data loss. Charge the phone, use a reliable USB cable, and make sure Windows has the BlackBerry USB driver needed to recognize it.
2. Connect only the device to be repaired. Unlock it and verify its model and device PIN. The PIN shown by the utility identifies the target device; do not publish device PINs, passwords, or backups.
3. Check the SHA-256 values below, then run `BlackBerryFix.exe`. This historical executable is unsigned. A matching hash establishes equality with the recorded file, not its safety or suitability for your device.
4. Confirm the device PIN shown by the utility and select **Fix this phone**. Wait for the result. On our device the first attempt requested disabling the device password and restarting the utility. If you see the same prompt, follow it on the phone and restore your previous security settings after the repair.
5. Once the tool reports completion, create a disposable test file or note. Restart normally, observe the LED, and check that the file persists. Create another and repeat the reboot check. **If data keeps disappearing, do not consider the repair verified.** Keep the external backup and investigate further.

This operation affects device data. Follow the utility's actual prompts, take your backup situation into account, and do not operate on other connected devices.

## Observed result

On 2026-11-09 (UTC) we used the Windows utility on one **BlackBerry Q10 SQN100-3 running BB10 10.3.3.3216**:

- The utility reported `Fixed`. The first restart had no blue LED, but both previously written test markers were still missing.
- Two newly created markers survived the second normal restart unchanged, again without a blue LED. A subsequently reinstalled app, backend, and phone-side backup also survived another restart.
- This is a single-device, limited-reboot observation. The first post-fix data loss and unknown long-term reliability remain material. Other models, OS versions, and the Mac utility have not been validated by this project.

## File integrity

```text
8dab7e156cf63062890e2eceda478d10de96d4918443422a7ee2740e860632a0  vendor/windows/BlackBerryFix.exe
74321fc83a8680a0a44ba6b842d1dc8883850b968414700b435dc2d93e3b8d67  vendor/windows/BlackBerryFix.zip
201f1338e86980d5b5cbd318b750fad387cbc0cdd2e08eaacf4a9a5c9eba742c  vendor/mac/KB36747_BlackBerryFixMac.zip
```

With Python 3 installed, run this from the repository root:

```powershell
python tools/verify.py
```

The verifier only reads files; it does not execute the utility or connect to the phone. It also checks the contents and CRC of both ZIP archives. On Windows, an individual file can be checked with:

```powershell
Get-FileHash -Algorithm SHA256 .\vendor\windows\BlackBerryFix.exe
```

Both ZIP hashes match recorded historical files: [Windows record](https://www.herdprotect.com/blackberryfix.zip-a733a48e28919fbb3f507e4f9e08fec3fb026d15.aspx) and [Mac record](https://www.herdprotect.com/kb36747_blackberryfixmac.zip-a316817eac09a7fbc2eaf9a107bc77532ed048f4.aspx). These records are not a vendor signature or a security audit. The historical knowledge-base article was [KB36747](https://www.blackberry.com/btsc/KB36747); its old link may no longer work.

## License and attribution

The project's original documentation and verification script are licensed under [MIT](LICENSE). The historical third-party BlackBerryFix files in `vendor/` are **not covered by that MIT license**. Their source code and license terms were not included, and permission to redistribute them has not been established. Rights remain with the respective rights holders; see [NOTICE.md](NOTICE.md).
