#!/bin/bash

for i in {59..76}; do
    # 1. Cambia "carpeta_$i" por el nombre real de tus directorios
    origen=/scratch_isilon/projects/0016-lucia/vicomtech_set2/LUCIA_"$i"
    destino="/scratch_isilon/groups/pbt/matt/transfers/LUCIA/batch_04"

    # 2. Verifica si el directorio origen existe antes de crear el link
    if [ -d "$origen" ]; then
        ln -s "$origen" "$destino"
        echo "✅ Enlace creado: $destino -> $origen"
    else
        echo "❌ Saltado: $origen no existe."
    fi
done

# after run this script
# nohup nice rsync -rvL --size-only ./batch_04 /ftp/downloads/LUCIA > LUCIA_batch4.log 2>&1
