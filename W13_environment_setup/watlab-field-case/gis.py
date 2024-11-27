from osgeo import ogr, osr

def get_polyline_coordinates_from_shapefile(
    shapefile_path: str,
    target_epsg: int = None,
    feature_index: int = 0
) -> tuple:
    """
    Reads polyline coordinates from a shapefile using GDAL.

    :param shapefile_path: The path to the shapefile.
    :type shapefile_path: str
    :param target_epsg: EPSG code of the target coordinate reference system (CRS).
                        If provided, coordinates will be transformed to this CRS.
                        Defaults to None (no transformation).
    :type target_epsg: int, optional
    :param feature_index: Index of the feature (polyline) to extract.
                          Defaults to 0 (first feature).
    :type feature_index: int, optional
    :return: Tuple of lists containing x_coords and y_coords.
    :rtype: tuple (list, list)

    :raises FileNotFoundError: If the shapefile cannot be opened.
    :raises ValueError: If the geometry type is unsupported.
    """
    # Open the shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.Open(shapefile_path, 0)  # 0 means read-only
    if data_source is None:
        raise FileNotFoundError(f"Could not open {shapefile_path}")
    else:
        print(f"Opened {shapefile_path}")

    # Get the layer and spatial reference
    layer = data_source.GetLayer()
    source_srs = layer.GetSpatialRef()

    # Define coordinate transformation if target_epsg is provided
    if target_epsg is not None:
        target_srs = osr.SpatialReference()
        target_srs.ImportFromEPSG(target_epsg)
        transform = osr.CoordinateTransformation(source_srs, target_srs)
    else:
        transform = None  # No transformation

    # Reset reading and get the feature by index
    layer.ResetReading()
    feature = layer.GetFeature(feature_index)
    if feature is None:
        raise IndexError(f"No feature found at index {feature_index}")

    geometry = feature.GetGeometryRef()
    geom_type = geometry.GetGeometryName()

    x_coords = []
    y_coords = []

    if geom_type == 'LINESTRING':
        num_points = geometry.GetPointCount()
        for i in range(num_points):
            x, y, _ = geometry.GetPoint(i)
            if transform:
                x, y, _ = transform.TransformPoint(x, y)
            x_coords.append(x)
            y_coords.append(y)
    elif geom_type == 'MULTILINESTRING':
        for line_index in range(geometry.GetGeometryCount()):
            line = geometry.GetGeometryRef(line_index)
            num_points = line.GetPointCount()
            for i in range(num_points):
                x, y, _ = line.GetPoint(i)
                if transform:
                    x, y, _ = transform.TransformPoint(x, y)
                x_coords.append(x)
                y_coords.append(y)
    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")

    # Close the data source
    data_source = None

    return x_coords, y_coords
