declare global {
  interface Window {
    google: typeof google;
    MarkerClusterer: {
      new (options: {
        map: any;
        markers: any[];
        algorithm?: any;
        renderer?: any;
      }): {
        clearMarkers(): void;
      };
      GridAlgorithm: {
        new (options: { maxZoom: number; gridSize: number }): any;
      };
    };
  }
}

declare namespace google.maps {
  class Map {
    constructor(mapDiv: HTMLElement, opts?: MapOptions);
    setCenter(latlng: LatLng | LatLngLiteral): void;
    setZoom(zoom: number): void;
    getZoom(): number | undefined;
    panTo(latlng: LatLng | LatLngLiteral): void;
    fitBounds(bounds: LatLngBounds): void;
    getBounds(): LatLngBounds | undefined;
    addListener(eventName: string, handler: Function): MapsEventListener;
  }

  class Marker {
    constructor(opts?: MarkerOptions);
    setMap(map: Map | null): void;
    addListener(eventName: string, handler: Function): MapsEventListener;
  }

  class LatLngBounds {
    constructor(sw?: LatLng | LatLngLiteral, ne?: LatLng | LatLngLiteral);
    extend(point: LatLng | LatLngLiteral): LatLngBounds;
    getCenter(): LatLng;
    getNorthEast(): LatLng;
    getSouthWest(): LatLng;
  }

  class LatLng {
    constructor(lat: number, lng: number);
    lat(): number;
    lng(): number;
  }

  class InfoWindow {
    constructor(opts?: InfoWindowOptions);
    setContent(content: string | Element): void;
    open(map?: Map, anchor?: Marker): void;
    close(): void;
  }

  class Size {
    constructor(width: number, height: number);
  }

  class Point {
    constructor(x: number, y: number);
  }

  interface MapOptions {
    center?: LatLng | LatLngLiteral;
    zoom?: number;
    styles?: MapTypeStyle[];
    mapTypeId?: MapTypeId;
    zoomControl?: boolean;
    mapTypeControl?: boolean;
    scaleControl?: boolean;
    streetViewControl?: boolean;
    rotateControl?: boolean;
    fullscreenControl?: boolean;
    gestureHandling?: string;
  }

  interface MarkerOptions {
    position?: LatLng | LatLngLiteral;
    map?: Map;
    title?: string;
    icon?: string | Icon | Symbol;
    animation?: Animation;
    zIndex?: number;
    label?: string | Label;
  }

  interface Label {
    text: string;
    color?: string;
    fontWeight?: string;
    fontSize?: string;
  }

  interface InfoWindowOptions {
    content?: string | Element;
    disableAutoPan?: boolean;
    maxWidth?: number;
  }

  interface LatLngLiteral {
    lat: number;
    lng: number;
  }

  interface Icon {
    url?: string;
    scaledSize?: Size;
    anchor?: Point;
    path?: string | SymbolPath;
    scale?: number;
    fillColor?: string;
    fillOpacity?: number;
    strokeColor?: string;
    strokeWeight?: number;
  }

  interface Symbol {
    path: string | SymbolPath;
    scale: number;
    fillColor: string;
    fillOpacity: number;
    strokeColor: string;
    strokeWeight: number;
  }

  interface MapTypeStyle {
    featureType?: string;
    elementType?: string;
    stylers?: Array<{ [key: string]: any }>;
  }

  enum MapTypeId {
    ROADMAP = 'roadmap',
    SATELLITE = 'satellite',
    HYBRID = 'hybrid',
    TERRAIN = 'terrain'
  }

  enum SymbolPath {
    CIRCLE = 0,
    FORWARD_CLOSED_ARROW = 1,
    FORWARD_OPEN_ARROW = 2,
    BACKWARD_CLOSED_ARROW = 3,
    BACKWARD_OPEN_ARROW = 4
  }

  enum Animation {
    BOUNCE = 1,
    DROP = 2
  }

  interface MapsEventListener {
    remove(): void;
  }

  namespace event {
    function addListenerOnce(instance: any, eventName: string, handler: Function): MapsEventListener;
  }

  class Geocoder {
    constructor();
    geocode(request: GeocoderRequest): Promise<GeocoderResult>;
  }

  class DirectionsService {
    constructor();
    route(request: DirectionsRequest): Promise<DirectionsResult>;
  }

  class DirectionsRenderer {
    constructor(options?: DirectionsRendererOptions);
    setDirections(result: DirectionsResult): void;
    setMap(map: Map | null): void;
  }

  interface DirectionsRequest {
    origin: LatLng | LatLngLiteral | string;
    destination: LatLng | LatLngLiteral | string;
    travelMode: TravelMode;
    unitSystem?: UnitSystem;
    waypoints?: DirectionsWaypoint[];
    optimizeWaypoints?: boolean;
    provideRouteAlternatives?: boolean;
    avoidHighways?: boolean;
    avoidTolls?: boolean;
    region?: string;
  }

  interface DirectionsResult {
    routes: DirectionsRoute[];
    geocoded_waypoints: DirectionsGeocodedWaypoint[];
  }

  interface DirectionsRoute {
    bounds: LatLngBounds;
    copyrights: string;
    fare: TransitFare;
    legs: DirectionsLeg[];
    overview_path: LatLng[];
    overview_polyline: string;
    warnings: string[];
    waypoint_order: number[];
  }

  interface DirectionsLeg {
    arrival_time: Time;
    departure_time: Time;
    distance: Distance;
    duration: Duration;
    duration_in_traffic: Duration;
    end_address: string;
    end_location: LatLng;
    start_address: string;
    start_location: LatLng;
    steps: DirectionsStep[];
    traffic_speed_entry: any[];
    via_waypoints: LatLng[];
  }

  interface DirectionsStep {
    distance: Distance;
    duration: Duration;
    end_location: LatLng;
    instructions: string;
    path: LatLng[];
    polyline: string;
    start_location: LatLng;
    transit: TransitDetails;
    travel_mode: TravelMode;
  }

  interface DirectionsGeocodedWaypoint {
    geocoder_status: GeocoderStatus;
    partial_match: boolean;
    place_id: string;
    types: string[];
  }

  interface DirectionsWaypoint {
    location: LatLng | LatLngLiteral | string;
    stopover: boolean;
  }

  interface DirectionsRendererOptions {
    map?: Map;
    suppressMarkers?: boolean;
    polylineOptions?: PolylineOptions;
  }

  interface PolylineOptions {
    strokeColor?: string;
    strokeWeight?: number;
    strokeOpacity?: number;
  }

  interface Time {
    text: string;
    time_zone: string;
    value: Date;
  }

  interface Distance {
    text: string;
    value: number;
  }

  interface Duration {
    text: string;
    value: number;
  }

  interface TransitFare {
    currency: string;
    value: number;
  }

  interface TransitDetails {
    arrival_stop: TransitStop;
    arrival_time: Time;
    departure_stop: TransitStop;
    departure_time: Time;
    headsign: string;
    headway: number;
    line: TransitLine;
    num_stops: number;
  }

  interface TransitStop {
    location: LatLng;
    name: string;
  }

  interface TransitLine {
    agencies: TransitAgency[];
    color: string;
    icon: string;
    name: string;
    short_name: string;
    text_color: string;
    url: string;
    vehicle: TransitVehicle;
  }

  interface TransitAgency {
    name: string;
    phone: string;
    url: string;
  }

  interface TransitVehicle {
    icon: string;
    local_icon: string;
    name: string;
    type: VehicleType;
  }

  enum TravelMode {
    DRIVING = 'DRIVING',
    WALKING = 'WALKING',
    BICYCLING = 'BICYCLING',
    TRANSIT = 'TRANSIT'
  }

  enum UnitSystem {
    METRIC = 0,
    IMPERIAL = 1
  }

  enum VehicleType {
    BUS = 'BUS',
    CABLE_CAR = 'CABLE_CAR',
    COMMUTER_TRAIN = 'COMMUTER_TRAIN',
    FERRY = 'FERRY',
    FUNICULAR = 'FUNICULAR',
    GONDOLA_LIFT = 'GONDOLA_LIFT',
    HEAVY_RAIL = 'HEAVY_RAIL',
    HIGH_SPEED_TRAIN = 'HIGH_SPEED_TRAIN',
    INTERCITY_BUS = 'INTERCITY_BUS',
    METRO_RAIL = 'METRO_RAIL',
    MONORAIL = 'MONORAIL',
    OTHER = 'OTHER',
    RAIL = 'RAIL',
    SHARE_TAXI = 'SHARE_TAXI',
    SUBWAY = 'SUBWAY',
    TRAM = 'TRAM',
    TROLLEYBUS = 'TROLLEYBUS'
  }
  
  interface GeocoderRequest {
    address?: string;
    location?: LatLng;
    bounds?: LatLngBounds;
    componentRestrictions?: GeocoderComponentRestrictions;
    region?: string;
  }
  
  interface GeocoderComponentRestrictions {
    country?: string;
    administrativeArea?: string;
    postalCode?: string;
    route?: string;
    locality?: string;
  }
  
  interface GeocoderResult {
    results: GeocoderResultItem[];
    status: GeocoderStatus;
  }
  
  interface GeocoderResultItem {
    address_components: GeocoderAddressComponent[];
    formatted_address: string;
    geometry: GeocoderGeometry;
    place_id: string;
    types: string[];
  }
  
  interface GeocoderAddressComponent {
    long_name: string;
    short_name: string;
    types: string[];
  }
  
  interface GeocoderGeometry {
    location: LatLng;
    location_type: GeocoderLocationType;
    viewport: LatLngBounds;
    bounds?: LatLngBounds;
  }
  
  enum GeocoderStatus {
    OK = 'OK',
    ZERO_RESULTS = 'ZERO_RESULTS',
    OVER_QUERY_LIMIT = 'OVER_QUERY_LIMIT',
    REQUEST_DENIED = 'REQUEST_DENIED',
    INVALID_REQUEST = 'INVALID_REQUEST',
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
  }
  
  enum GeocoderLocationType {
    ROOFTOP = 'ROOFTOP',
    RANGE_INTERPOLATED = 'RANGE_INTERPOLATED',
    GEOMETRIC_CENTER = 'GEOMETRIC_CENTER',
    APPROXIMATE = 'APPROXIMATE'
  }

  namespace places {
    class Autocomplete {
      constructor(input: HTMLInputElement, opts?: AutocompleteOptions);
      addListener(eventName: string, handler: Function): MapsEventListener;
      getPlace(): PlaceResult;
      setBounds(bounds: LatLngBounds): void;
      setComponentRestrictions(restrictions: ComponentRestrictions): void;
      setFields(fields: string[]): void;
      setOptions(options: AutocompleteOptions): void;
      setTypes(types: string[]): void;
    }
  }

  class Autocomplete {
    constructor(input: HTMLInputElement, opts?: AutocompleteOptions);
    addListener(eventName: string, handler: Function): MapsEventListener;
    getPlace(): PlaceResult;
    setBounds(bounds: LatLngBounds): void;
    setComponentRestrictions(restrictions: ComponentRestrictions): void;
    setFields(fields: string[]): void;
    setOptions(options: AutocompleteOptions): void;
    setTypes(types: string[]): void;
  }

  interface AutocompleteOptions {
    bounds?: LatLngBounds;
    componentRestrictions?: ComponentRestrictions;
    fields?: string[];
    strictBounds?: boolean;
    types?: string[];
  }

  interface ComponentRestrictions {
    country?: string | string[];
  }

  interface PlaceResult {
    address_components?: GeocoderAddressComponent[];
    formatted_address?: string;
    geometry?: PlaceGeometry;
    icon?: string;
    name?: string;
    photos?: PlacePhoto[];
    place_id?: string;
    plus_code?: PlacePlusCode;
    types?: string[];
    url?: string;
    utc_offset?: number;
    vicinity?: string;
    website?: string;
  }

  interface PlaceGeometry {
    location?: LatLng;
    viewport?: LatLngBounds;
  }

  interface PlacePhoto {
    height: number;
    html_attributions: string[];
    width: number;
    getUrl(opts?: PhotoOptions): string;
  }

  interface PhotoOptions {
    maxHeight?: number;
    maxWidth?: number;
  }

  interface PlacePlusCode {
    compound_code?: string;
    global_code: string;
  }

  // Advanced Marker API (if available)
  namespace marker {
    class AdvancedMarkerElement {
      constructor(opts?: AdvancedMarkerOptions);
      addListener(eventName: string, handler: Function): MapsEventListener;
    }

    class PinElement {
      constructor(opts?: PinElementOptions);
      element: Element;
    }

    interface AdvancedMarkerOptions {
      position?: LatLng | LatLngLiteral;
      map?: Map;
      title?: string;
      content?: Element;
    }

    interface PinElementOptions {
      background?: string;
      borderColor?: string;
      glyphColor?: string;
      scale?: number;
    }
  }
}

 