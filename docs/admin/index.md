# Admin

There are two types of administrators for SmartAC backend: Superusers and Staff users. Superusers have all permissions to do everything possible in the admin interface. Staff users have the ability to view/update/create/delete devices and their related records as well as view/update/create/delete user invitations.

# Invitations

Invite another user to the backend by going to the "Invitations" section of the admin and tapping the "Add Invitation" button. Fill out the form with the email address of the user to invite and they will receive an invitation email. Clicking the link in the invitation email will allow them to sign up for an admin account. Only those with such a link can create an account. After signup they will have all the permissions of a Staff user, and can invite other users. A superuser can find the new user in the "Users" section of the admin and upgrade it to a superuser if desired.

*Note to testers*: If you open the link in a browser that is already logged in to the admin, the link will not work. It's best to open the link in an incognito window or different browser.

# Users

Superusers have view/update/create/delete priveleges on any user record. They can upgrade a user to superuser status by selecting the "Superuser status" on the edit user form. They can deactivate or reactivate any user account by unchecking or rechecking the "Active" checkbox on the edit user form.

# Devices

The "Devices" section of the admin interface allows admins to view/update/create/delete device records as well as their sensor logs, status updates, and auth tokens. Select "Devices" to view a list of all devices. You can search for devices by serial number on this page, as well as filter to show devices that are alerting. Devices that are alerting satisfy one of the following criteria:

  - The latest carbon monoxide reading is > 9 PPM
  - The device's latest health status is one of
    - "needs_service", "needs_new_filter" or "gas_leak."