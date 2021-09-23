# some proguard confusion sample. 
# https://www.guardsquare.com/manual/configuration/usage

RT_JAR=$JAVA_HOME/jre/lib/rt.jar
PROGUARD_FILE="lab.pro"

# check files exit status
[ ! -e $RT_JAR ] && echo "not exit $RT_JAR" && exit 2
[ ! -e $PROGUARD_FILE ] && echo "not exit $PROGUARD_FILE" && exit 2
 
rm -rf build
mkdir build

echo "exec *.java >>> *.class ..."
find . -name '*.java' |
    xargs -t javac # -d build/classes
[ $? != 0 ] && echo "exit ..." && exit 2

echo ""
echo "exec *.class >>> *.jar ..."
find . -name '*.class' |
    xargs -t jar cvf build/classes.jar
[ $? != 0 ] && echo "exit ..." && exit 2

echo ""
echo "exec proguard injar >>> outjar ..."
../../bin/proguard/bin/proguard.sh \
    -libraryjars $RT_JAR \
    -include $PROGUARD_FILE \
    -injars build/classes.jar \
    -outjars build/classes_proguard.jar
[ $? != 0 ] && echo "proguard exit..." && exit 2

echo ""
echo "exec inflating outjar ..."
find . -name '*.class' -delete
unzip build/classes_proguard.jar -d build/classes_proguard