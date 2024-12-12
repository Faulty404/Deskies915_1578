# /gestureModel/data_collection

if [ $# -ne 1 ]; then
	echo "Error: Not enough arguments"
	echo "Usage: ./many_photos.sh <path_to_directory_photos>/"
	echo -e "Note that the ending forward slash is required to be in the name\nFor example, the name \"~/Pictures/\" is valid but \"~/Pictures\" is not"
	echo ""
	exit 1
fi

photos=($(ls $1))
script="./collection.py"

for photo in "${photos[@]}"; do
	python3 "$script" "./$1$photo"
done
