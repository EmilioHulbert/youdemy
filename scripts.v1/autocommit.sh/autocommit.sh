cd /home/hulbert/Desktop/
cp Tech.md B00kOfProblems/
cd B00kOfProblems
cp Tech.md Readme.md
git add *
git status
git remote add origin https://github.com/lilplucky/Book0fProblems.git
git remote set-url origin https://lilplucky:GITHUB_PERSONAL_ACCESS_TOKEN@github.com/lilplucky/B00kOfProblems.git
git commit -m "Updated $(date)"
git push origin master

