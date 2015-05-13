cd /Users/Matthew/programming/prove-math &&

babel www/scripts6/lib/profile.js > www/scripts/lib/profile.js &&

babel www/scripts6/main.js > www/scripts/main.js &&

# node build/r.js -o mainConfigFile=www/scripts/main.js baseUrl=www/scripts/lib name=../main out=www/scripts/main-optimized.min.js generateSourceMap=true preserveLicenseComments=false optimize=uglify2 &&
# no need to optimize

echo 'done updating files on local machine' &&


# cd /Users/Matthew/programming &&

# scp -i ~/programming/amazon/berry/berry.pem -r ./prove-math/* ec2-user@54.174.141.44:prove-math/ &&

# echo 'done updating files on server' &&

# open http://54.174.141.44:7766/index.html &&


echo 'done.'
