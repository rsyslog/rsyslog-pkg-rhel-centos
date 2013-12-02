!#/bin/sh
BRANCHES="v5-stable v6-stable v6-beta v7-stable v7-beta v7-devel v8-devel testing"

echo "-------------------------------------"
echo "--- Upload RPM Packages               ---"
echo "-------------------------------------"
echo "Which BRANCH do you want to upload?--"
select szBranch in $BRANCHES
do
        echo "Uploading Branch '$szBranch'
        "
        break;
done

# scp -r /home/makerpm/yumrepo/$szBranch/* makerpm@vserver.adiscon.com:/home/makerpm/yumrepo/$szBranch/
rsync -au -e ssh --progress /home/makerpm/yumrepo/$szBranch/* makerpm@vserver.adiscon.com:/home/makerpm/yumrepo/$szBranch/




