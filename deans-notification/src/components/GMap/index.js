import React, { Component } from "react";
import { connect } from "react-redux";
import Marker from "@components/Marker";
import PropTypes from "prop-types";
import GoogleMapReact from "google-map-react";
import { geocodeByAddress, getLatLng } from "react-places-autocomplete";

class GMap extends Component {
  state = {
    crises: {}
  };

  componentDidMount = () => {
    this.loadCrisesIntoState();
  };

  componentDidUpdate = prevProps => {
    if (prevProps.crises !== this.props.crises) {
      this.loadCrisesIntoState();
    }
  };

  createMarker = () => {
    const { crises } = this.state;
    const { crisisType } = this.props;
    if (Object.keys(crises).length === 0) return null;
    return Object.keys(crises).map(index => {
      const crisis = crises[index];
      const lat = crisis.lat;
      const lng = crisis.lng;
      const type = crisis.type;
      const location = crisis.location;
      const description = crisis.description;
      return (
        <Marker
          key={index}
          lat={lat}
          lng={lng}
          type={type}
          location={location}
          crisisType={crisisType || []}
          description={description}
        />
      );
    });
  };

  loadCrisesIntoState = () => {
    // this.setState({ crises: {} }); // clear cached crisis
    this.props.crises.forEach(crisis => {
      const id = crisis.crisis_id;
      const type = crisis.crisis_type;
      const description = crisis.crisis_description;
      geocodeByAddress(crisis.crisis_location1)
        .then(geoCode => getLatLng(geoCode[0]))
        .then(location => {
          this.setState({
            crises: {
              ...this.state.crises,
              [id]: {
                lat: location && location["lat"],
                lng: location && location["lng"],
                location: crisis.crisis_location1,
                type: type,
                description: description
              }
            }
          });
        });
    });
  };

  render() {
    return (
      // Important! Always set the container height explicitly
      <div style={{ height: "100%", width: "100%" }}>
        <GoogleMapReact
          bootstrapURLKeys={{
            key: "AIzaSyA4Z60Vt8Bq84x2X32NQ286a_2_hADWzqI"
          }}
          defaultCenter={{ lat: 1.3354, lng: 103.8277 }}
          defaultZoom={12}
          draggable={true}
        >
          {this.createMarker()}
        </GoogleMapReact>
      </div>
    );
  }
}

GMap.propTypes = {
  crises: PropTypes.array.isRequired,
  crisisType: PropTypes.array
};

const mapStateToProps = state => {
  const { system } = state;
  return {
    crisisType: system && system.crisisType
  };
};

export default connect(mapStateToProps)(GMap);
