# Blogin

Blogin is a personal blog website that base on flask development.

## Introduce

The personal blog site developed by the Flask Python Web framework consists of two parts: the front-end and the back-end.

### Front-end

1. **Personal Blog**
   - Support blog categorization
   - Support comment 
   - Support  share your blog to personal social network
   - Support blog archive
2. **Personal Gallery**
   - Support photo tag
   - Support comment and like
   - Support share your photo to personal social network
3. **Online Lite Tool**
   - Online word cloud graph generator
   - Online multi translation tool
   - Online Tang-Song poem search tool
   - Online ocr tool
   - Online IP real address search tool
4. **Comment System**
   - Support comment/delete/report
   - Support reply comment
5. **Personal Profile**
   - Personal profile card
   - Message notifycation
   - Modify your information
   - Record login log
6. **Tang-Song Poem**
   - Get a Tang-Song poem with random way
   - Get Song Ci with random way
   - Supply API to get Tang-Song poem
7. **Others**
   - Support make personal plan recently
   - Support the contribution heat map display for the past three months

### Back-end

1. **Content manage**
   - **Blog** 
     - Create blog
     - Modify blog
     - Delete blog(It's just masking the display on the front page, not actually deleting it from the database)
   - **Gallery**
     - Add photo
     - Modify Photo
     - Delete Photo(like blog)
   - **Literature**
     - Tang-Song poem
       - Modify(todo)
       - New(todo)
   - **Personal Plan**
     - Add a new personal plan
     - Modify personla plan
     - Finish personal plan
2. **Social Mange**
   - **Comment Manage**
     - Look up comments
     - Delete comment(like blog)
   - **User Manage**
     - Look up users
     - Ban user account