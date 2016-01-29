### Code Contribute Process

Personally, I highly recommend our team members to use Linux like system, such as ubuntu, MacOS, etc., to coding, because we are using git as our vision control tools, most of the operations would be in command line mode. 

I have seted up the online code review system, and would send you a invitation email to register. And the following is some instructions about how to use `git` and how to use this code review system. 

1. Set up local working directory.  Open terminal, go to some place you would like to store the code. Attention that this repo is a private repo, so git may ask for your username and password again and again. To avoid this situation, manipulate `config` file under `.git` directory to set up your user name and password. 
   
   ``` bash
   git clone https://github.com/bbemis017/Saturn
   ```
   
2. Install Phabricator, which is a code review system used by Facebook, and developed by a Facebook engineer. Recommend to install it under `~/` directory. Then add `~/arcanist/bin/` into your PATH environment variable.
   
   ``` bash
   git clone https://github.com/phacility/libphutil.git
   git clone https://github.com/phacility/arcanist.git
   ```
   
3. Then to configure local development environment. Everyone are going to have a local development environment which would help us to test our code while developing. The local development environment would include database and python environments, which would discuss further in the future. 
   
4. When start to coding a new feature, use command
   
   ``` bash
   git checkout -b “new_branch_name”
   ```
   
   This would create a new branch in your local machine. Master would be our main branch that we need do changes on other branches, and merge to master after review.
   
5. Then do some changes. Please do not commit too many times while developing one feature. While coding, just do changes, save files, but do not commit. Just commit change only once after you finish all the code on this feature. This would make backtrace more easier if something goes wrong. 
   
6. Then commit your work by 
   
   ``` bash
   git add .
   git commit -m "<message>"
   ```
   
   Then use arc command to submit your work for colleague to review
   
   ``` bash
   arc diff
   ```
   
   Here `arc diff` would ask for some informations. Fill in Summary. For Test Plan, it's okay to just put "No". Then reviewer, put your colleague's username on `http://phab.mrha1f.com`. For subscriber, maybe put Ben's username to let the project leader know our progress. Then there would generate a url on website about your diff, and there would be a id about it, for example `D100`. And both reviewer and subscriber would receive a email about you have submitted a diff. 
   
7. Wait for feedbacks from you colleague. If your colleague request you to do some change, you need to fix them accordingly. Then you need to commit your code again. Attention that you need type:
   
   ``` bash
   git add .
   git commit --amend
   ```
   
   `--amend` would overwrite your former commit.  Then you can diff again by:
   
   ``` bash
   arc diff --update D100
   ```
   
   `--update` flag indicates you're updating one diff. But if you are in the same brach, `arc diff` would also works. Then reviewer would review your code again. 
   
8. If there your colleague think you did really good job and nothing's gonna change. You can just push your code.
   
   ``` bash
   arc land
   ```
   
9. Get some sleep. :p