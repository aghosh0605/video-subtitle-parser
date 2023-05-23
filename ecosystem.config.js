module.exports = {
  apps: [
    {
      name: "Ecowiser Frontend",
      script: "./run.sh",
    },
    {
      name:"Ecowiser:Backend",
      script:"./run-backend.sh",
    },
    {
      name:"Ecowiser:Celery",
      script:"./run-celery.sh"
    }
  ],
};
