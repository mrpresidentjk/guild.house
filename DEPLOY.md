Guild Website Deployment Instructions
---

(for future me)


Code repository is kept at `bitbucket` as a backup.


####Sun Apr 09 10:36:06 AEST 2017
==========

Status:

3x things going on in git:

###`development-registration`
What I want to be working on now, implementing allauth.

`development` branch is going to get left behind temporarily.


###`production`/`live/production`

Turned off `Bookings` system on live site. We still want this *on* for the dev.guild.house.

These branches with this single commit will be left dangling until ready to release `Bookings` and whatever.

Repeat: nothing will happen with these branches until next release.


###`master`/`dev/production`
Per above, this is going to be dev/staging where new features, etc will be tested.

This will track `development`/`development-registration`.


---

Website Features
---

Apps in project:

**Existing:**

* `Users`
* `Flatpages`
* `Sites`
* `Robots`
* `Tags`
* `Homepage`
* `Treemenues`
* `Redirects`
* `Blog`

**In Development:**

* `Menus`
* `Library`
* `Bookings`
* *Style refresh (relaunch)*

**Proposed**

* `Events` -- `Matches`
* `Purchases`
* `Members`
* `Votes` (potentially feature of `Library`)
