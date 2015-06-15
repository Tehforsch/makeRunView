# WE META NOW
echo $(pwd)
when-changed modules/pymodule.py modules/texmodule.py modules/gpimodule.py makeRunView/dependencymanager.py makeRunView/config.py makeRunView/dependency.py makeRunView/executor.py makeRunView/filestate.py makeRunView/main.py makeRunView/makerunview.py makeRunView/observer.py makeRunView/tools.py makeRunView/utils/osUtils.py makeRunView/utils/fileUtils.py test/testtools.py test/testmakerunview.py -c "nosetests --with-coverage"
