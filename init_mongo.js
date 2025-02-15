var config = {
    _id: 'lsmdb',
    members: [
      { _id: 0, host: 'mongo_machine1:27017', priority: 5 },
      { _id: 1, host: 'mongo_machine2:27017', priority: 2 },
      { _id: 2, host: 'mongo_machine3:27017', priority: 1 }
    ]
  };
  rs.initiate(config);
  rs.status();  