'use strict';
import React from "react";

import {GoogleMap, withGoogleMap, Marker} from "react-google-maps";
import Polygon from "../Polygon";


export default withGoogleMap(props => {
    return <GoogleMap
        ref={props.onMapLoad}
        defaultZoom={props.zoom}
        defaultCenter={props.center}
        mapTypeId={props.mapTypeId}
        options={props.options}
        onClick={props.onMapClick}
    >
        {props.polygons.map(polygon => (
            <Polygon key={polygon.options.id} {...polygon} />
        ))}
        <Marker {...props.marker}/>
    </GoogleMap>
});
