#######################################
# Parse a YAML configuration file and return key value pairs.
# Arguments:
#   filename: name of a yaml configuration parameter file
#   env: the environment, dev, ppd, prd
#   prefix: a prefix for the resolving variable names
# Returns
#   key="value"
# Usage after source:
#   eval $(parse_configuration config.yml)
#   echo $variable
#######################################
function parse_config() {
   local filename=$1
   local env=$2
   local netenv
   # Netowrk environment is nonprod: np, prod: p
   # Network environment is a higher level construct
   if [ "$env" == "dev" ]; then
      netenv="np"
   elif [ "$env" == "ppd" ] || [ "$env" == "prd" ]; then
      netenv="p"
   else
      echo "invalid"
      return 1
   fi
   # Can be passed to add a prefix to all variables
   local prefix=$3
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @ | tr @ '\034')
   sed -ne "s|^\($s\):|\1|" \
      -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
      -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p" $1 |
      sed "s|<env>|$env|g" |
      sed "s|<netenv>|$netenv|g" |
      awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}

#######################################
# Parse a arguments to a shell script
# Arguments:
#   -e | --env: the environment, dev, ppd, prd
#   -n | --name: the name of the job
# Returns
#   none
# Usage:
#   parse_args "$@"
#######################################
function parse_args() {
   POSITIONAL=()
   while [[ $# -gt 0 ]]; do
      key="$1"

      case $key in
      -e | --env)
         env="$2"
         shift # past argument
         shift # past value
         ;;
      -n | --name)
         name="$2"
         shift # past argument
         shift # past value
         ;;
      *)                    # unknown option
         POSITIONAL+=("$1") # save it in an array for later
         shift              # past argument
         ;;
      esac
   done
   set -- "${POSITIONAL[@]}" # restore positional parameters

   echo env = "${env}"
}
