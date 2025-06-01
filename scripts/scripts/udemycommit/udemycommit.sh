cd /home/hulbert/Desktop/youdemy
git add .
git commit -m "My learning As Of  $(date)"
git branch -M development
git remote add origin https://github.com/lilplucky/youdemy.git
git remote set-url origin https://lilplucky:GITHUB_PERSONAL_ACCESS_TOKEN_HERE@github.com/lilplucky/youdemy.git
git push -u origin development

