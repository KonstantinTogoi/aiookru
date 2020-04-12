REST API
========

List of all methods is available here: https://apiok.ru/en/dev/methods/rest/.

Executing requests
------------------

For executing API requests call an instance of :code:`APIMethod` class.
You can get it as an attribute of :code:`API` class instance or other :code:`APIMethod` class instance.

.. code-block:: python

    from aiookru import API

    api = API(session)

    events = await api.events.get()  # events for current user
    friends = await api.friends.get()  # current user's friends

Under the hood each API request is enriched
with parameters (https://apiok.ru/en/dev/methods/):

* :code:`application_key`
* :code:`format`
* :code:`method`
* :code:`sig`
* :code:`access_token`

to authorize request.

Methods
-------

.. |br| raw:: html

    <br/>

:superscript:`*` - only for Android and iOS applications, for external applications is required.

apps
~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *checkVipOfferStatus*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getAppPromoInfo*
      - prohibited
      - VALUABLE_ACCESS
    * - *getPlatformCatalogNodeTop*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getPlatformCatalogNodesTop*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getPlatformNew*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getPlatformTop*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getTop*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *removeAppPromoInfo*
      - prohibited
      - VALUABLE_ACCESS
    * - *setAppPromoInfo*
      - prohibited
      - VALUABLE_ACCESS
    * - *setVipOfferStatus*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *setVipOffers*
      - OAuth / WEB
      - VALUABLE_ACCESS

bookmark
~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *add*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *delete*
      - OAuth / WEB
      - VALUABLE_ACCESS

callbacks
~~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *payment*
      - prohibited
      - VALUABLE_ACCESS

communities
~~~~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *getMembers*
      - OAuth / WEB
      - VALUABLE_ACCESS

discussions
~~~~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *get*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getAttachedResources*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getComment*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getCommentLikes*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getComments*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getDiscussionComments*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getDiscussionCommentsCount*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getDiscussionLikes*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getDiscussions*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getDiscussionsNews*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getList*
      - OAuth / WEB
      - VALUABLE_ACCESS

events
~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *get*
      - OAuth / WEB
      - VALUABLE_ACCESS

friends
~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *appInvite*
      - OAuth / WEB
      - APP_INVITE
    * - *get*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getAppUsers*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getAppUsersOnline*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getBirthdays*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getByDevices*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getMutualFriends*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getOnline*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getRelatives*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getRelativesV2*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getSuggestions*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS

group
~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *getCounters*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *getInfo*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *getMembers*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getStatOverview*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getStatPeople*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getStatTopic*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getStatTopics*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getStatTrends*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getUserGroupsByIds*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *getUserGroupsV2*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *pinGroupFeed*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *setMainPhoto*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT,PHOTO_CONTENT

interests
~~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *get*
      - OAuth / WEB
      - VALUABLE_ACCESS

market
~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *add*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *addCatalog*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *delete*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *deleteCatalog*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *edit*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *editCatalog*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getByCatalog*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getByIds*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getCatalogsByGroup*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getCatalogsByIds*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *getProducts*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *pin*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *reorder*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *reorderCatalogs*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *setStatus*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT
    * - *updateCatalogsList*
      - OAuth / WEB
      - VALUABLE_ACCESS,GROUP_CONTENT

mediatopic
~~~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *getByIds*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getPollAnswerVoters*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getRepublishedTopic*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *post*
      - OAuth / WEB / Without Session :superscript:`*`
      -

notifications
~~~~~~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *sendFavPromo*
      - prohibited
      - VALUABLE_ACCESS
    * - *sendMass*
      - prohibited
      - VALUABLE_ACCESS
    * - *sendSimple*
      - prohibited
      - VALUABLE_ACCESS
    * - *stopFavPromo*
      - prohibited
      - VALUABLE_ACCESS
    * - *stopSendMass*
      - prohibited
      - VALUABLE_ACCESS
    * - *updateFavPromo*
      - prohibited
      - VALUABLE_ACCESS

payment
~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *appCashback*
      - prohibited
      - VALUABLE_ACCESS
    * - *getUserAccountBalance*
      - OAuth / WEB
      -
    * - *getUserAccountBonusBalance*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getVipStatus*
      - OAuth / WEB
      - VALUABLE_ACCESS

photos
~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *addAlbumLike*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT,LIKE
    * - *addPhotoLike*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT,LIKE
    * - *createAlbum*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *deleteAlbum*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *deletePhoto*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *deleteTags*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *editAlbum*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *editPhoto*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getAlbumInfo*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getAlbumLikes*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getAlbums*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getInfo*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getPhotoInfo*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getPhotoLikes*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getPhotoMarks*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getPhotos*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getTags*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getUserAlbumPhotos*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *getUserPhotos*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,PHOTO_CONTENT
    * - *setAlbumMainPhoto*
      - OAuth / WEB
      - VALUABLE_ACCESS,PHOTO_CONTENT

photosV2
~~~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *commit*
      - OAuth / WEB / Without Session :superscript:`*`
      - PHOTO_CONTENT
    * - *getUploadUrl*
      - OAuth / WEB / Without Session :superscript:`*`
      - PHOTO_CONTENT

places
~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *reverseGeocode*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *validate*
      - OAuth / WEB
      - VALUABLE_ACCESS

sdk
~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *getEndpoints*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getInstallSource*
      - prohibited
      - VALUABLE_ACCESS
    * - *getNotes*
      - prohibited
      - VALUABLE_ACCESS
    * - *init*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *reportPayment*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *reportStats*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *resetNotes*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *sendNote*
      - OAuth / WEB
      - VALUABLE_ACCESS

search
~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *tagContents*
      - OAuth / WEB
      -
    * - *tagMentions*
      - OAuth / WEB
      -
    * - *tagSearch*
      - OAuth / WEB
      -

share
~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *fetchLink*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *fetchLinkV2*
      - OAuth / WEB
      - VALUABLE_ACCESS

stream
~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *delete*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *isSubscribed*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *markAsSpam*
      - OAuth / WEB
      - VALUABLE_ACCESS

url
~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *getInfo*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS

users
~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *deleteGuests*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getAdditionalInfo*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getCallsLeft*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *getCurrentUser*
      - OAuth / WEB
      - GET_EMAIL
    * - *getGames*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getGuests*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getHolidays*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getInfo*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getInfoBy*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getInvitableFriends*
      - OAuth / WEB
      - VALUABLE_ACCESS
    * - *getLoggedInUser*
      - OAuth / WEB
      -
    * - *getMobileOperator*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *hasAppPermission*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *isAppUser*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *removeAppPermissions*
      - OAuth / WEB / Without Session :superscript:`*`
      -
    * - *setStatus*
      - OAuth / WEB
      - SET_STATUS
    * - *updateMask*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *updateMasks*
      - prohibited
      -
    * - *updateMasksV2*
      - prohibited
      -

video
~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *delete*
      - OAuth / WEB
      - VALUABLE_ACCESS,VIDEO_CONTENT
    * - *getUploadUrl*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,VIDEO_CONTENT
    * - *subscribe*
      - OAuth / WEB
      - VALUABLE_ACCESS,VIDEO_CONTENT
    * - *update*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS,VIDEO_CONTENT

widget
~~~~~~

.. list-table::
    :widths: 33 33 34
    :header-rows: 1

    * - **method**
      - **Session**
      - **Required permissions**
    * - *getWidgetContent*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
    * - *getWidgets*
      - OAuth / WEB / Without Session :superscript:`*`
      - VALUABLE_ACCESS
