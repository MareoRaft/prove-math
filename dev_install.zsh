#!/bin/zsh
# Developer install script

os=$(uname)
if [[ "$os" == "Darwin" ]]; then
	package_manager="brew"
elif [[ "$os" == "FreeBSD" ]]; then
	package_manager="pkg"
elif [[ "$os" == "Linux" ]]; then
	package_manager="apt-get"
else
	echo "operating system not recognized."
	return
fi

is_installed () {
	name=$1

	bool=1
	out=$(which "$name")
	if [[ "$out" == "$name not found" ]]
	then
		bool=0
	fi
	echo -n "$bool"
}

# compass
"$package_manager" install ruby
gem -v
gem update --system
gem install sass
sass -v
gem install compass
gem list | grep compass

# gulp + babel
"$package_manager" install node
npm -v
npm install gulp-cli -g
npm install gulp -D
gulp_deps=(babel-preset-es2015 gulp-babel gulp-for-compass gulp-autoprefixer child_process)
for gulp_dep in $gulp_deps
do
	npm install "$gulp_dep"
done
npm install --save-dev babel-cli

# python 3 + libraries
"$package_manager" install python3
"$package_manager" install wget
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
py_deps=(tornado networkx pytest requests_oauthlib colorlog pymongo)
for py_dep in $py_deps
do
	pip3 install "$py_dep"
done

# auth secrets
echo 'ask Matt for the file'

# report success (gulp_deps and py_deps not verified here, nor auth_secrets.txt)
dep_names=(ruby gem sass compass node npm gulp babel python3 wget pip3)
for dep_name in $dep_names
do
	dep_installed=$(is_installed "$dep_name")
	if [[ "$dep_installed" == "0" ]]
	then
		echo "$dep_name is not installed."
	fi
done
