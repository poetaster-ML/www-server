#!/bin/sh

echo ''
echo 'Pivotal Client'
echo ''

COMMAND="$1"
shift
case "$COMMAND" in

        build)
          yarn nuxt build
          ;;

        serve_local)
            yarn install
            yarn run dev
            ;;

        serve)
            yarn nuxt start
            ;;

        *)
            echo $"Usage: $0 {build|serve_local}"
            exit 1
esac
