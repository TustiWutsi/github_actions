# pour créer l'image test_authent
cd test_authent/
docker image build -t test_authent .

# pour créer l'image test_author
cd test_author/
docker image build -t test_author .

# pour lancer le docker-compose
docker-compose up

# pour vérifier les logs dans le volume
sudo cat /var/lib/docker/volumes/my_volume/_data/api_test.log