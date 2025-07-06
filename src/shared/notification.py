import subprocess

from src.shared.log import log_to_file
from src.shared.system_info import SystemInfo
from src.shared.term import warn


def send_notification(title: str, message: str, sys_info: SystemInfo):
    if sys_info["os"] == "linux":
        try:
            subprocess.run(["notify-send", title, message], check=True)
        except FileNotFoundError:
            warn("`notify-send` not found. Install it with: sudo apt install libnotify-bin")
        except Exception as e:
            log_to_file('warn', f"Notification failed: {str(e)}")

    elif sys_info["os"] == "darwin":
        try:
            subprocess.run([
                "osascript", "-e",
                f'display notification "{message}" with title "{title}"'
            ], check=True)
        except Exception as e:
            log_to_file('warn', f"Notification failed: {str(e)}")

    elif sys_info["os"] == "windows":
        try:
            powershell_cmd = f'''
                [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;
                $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);
                $textNodes = $template.GetElementsByTagName("text");
                $textNodes.Item(0).AppendChild($template.CreateTextNode("{title}")) > $null;
                $textNodes.Item(1).AppendChild($template.CreateTextNode("{message}")) > $null;
                $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("XVM");
                $notification = [Windows.UI.Notifications.ToastNotification]::new($template);
                $notifier.Show($notification)
            '''
            subprocess.run(["powershell", "-NoProfile", "-Command", powershell_cmd], check=True)
        except Exception as e:
            log_to_file('warn', f"Notification failed: {str(e)}")
