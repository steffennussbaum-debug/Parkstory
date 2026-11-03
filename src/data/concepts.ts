/**
 * Shared storytelling for the three homepage design concepts
 * (src/pages/concepts/*). Every concept tells the same story in its own
 * visual language, so the copy lives here once.
 *
 * Facts and figures are taken only from Parkstory's existing material (the
 * "How TilePark works" page) or from the positioning brief. Nothing here is a
 * project reference, certification or testimonial. Items under `future` are
 * directions, not product claims, and are labelled as such on every page.
 */

export const concepts = [
  {
    slug: 'architectural-future',
    letter: 'A',
    name: 'Architectural Future',
    summary: 'Minimalist, bright and elegant. The building comes first; the technology is drawn, not shouted.',
  },
  {
    slug: 'technological-disruption',
    letter: 'B',
    name: 'Technological Disruption',
    summary: 'Bold, cinematic, high contrast. A new category announced with full-screen statements and motion.',
  },
  {
    slug: 'industrial-intelligence',
    letter: 'C',
    name: 'Industrial Intelligence',
    summary:
      'Premium European engineering. Precision manufacturing, software and robotics presented like a specification.',
  },
] as const;

export const shift = {
  eyebrow: 'Parkstory · TilePark',
  title: 'Tomorrow’s infrastructure cannot run on yesterday’s technology.',
  lead: 'Parking infrastructure is a decision measured in decades. The technology behind it shouldn’t belong to the past.',
  intro:
    'TilePark is Parkstory’s new architecture for automated parking: a floor of independent conveyors that moves every car horizontally, and stackers that move it vertically. No ramps, no driving aisles, and no central machine that every car depends on.',
  points: [
    { n: '01', text: 'Automated parking is undergoing a technological transformation.' },
    { n: '02', text: 'TilePark is a new architecture, designed for the cities and buildings of tomorrow.' },
    { n: '03', text: 'The system you choose today will shape the building for decades.' },
  ],
};

export const question = {
  eyebrow: 'The question',
  title: 'What if the parking system you install today is already becoming obsolete?',
  body: 'A building is designed around its parking. Ramps, driving aisles, lift cores and shuttle lanes are built into the structure, and they stay there for the life of the building. The technology chosen at the start sets the limits for everything that follows.',
  constraints: [
    {
      k: 'Building design',
      v: 'Fixed ramps, aisles and lift cores dictate the layout, the column grid and the floor heights around them.',
    },
    {
      k: 'Space',
      v: 'In a conventional garage, roughly half of the floor area is taken up by ramps and driving lanes.',
    },
    {
      k: 'Flexibility',
      v: 'A layout organised around one shuttle aisle or one lift core is difficult to change once it has been built.',
    },
    {
      k: 'Operations',
      v: 'When the one machine every car depends on stops, every car behind it waits.',
    },
  ],
  timeline: {
    stages: ['Decision', 'Design & permits', 'Construction', 'Opening day', 'Decades of operation'],
    conventional: 'Frozen at the state of the day it was chosen',
    tilepark: 'Keeps receiving updates and new capabilities',
    note: 'Years pass between the first sketch and opening day. A technology chosen today is already years old when the first car arrives.',
  },
};

export const breakthrough = {
  eyebrow: 'The breakthrough',
  title: 'Not a better machine. A different architecture.',
  body: 'Conventional automated garages move cars with a few central machines along fixed paths. TilePark turns the floor itself into the machine.',
  principles: [
    {
      n: '01',
      k: 'Every position moves',
      v: 'The floor is a grid of conveyors. Each car rests on its own pallet and is moved lengthwise and crosswise, like a tile in a sliding puzzle.',
    },
    {
      n: '02',
      k: 'No central control',
      v: 'Each conveyor has its own controller and hands cars to its neighbours. There is no master computer, shuttle or lift that every car depends on.',
    },
    {
      n: '03',
      k: 'A new route every time',
      v: 'For every request the system calculates the route for the grid’s current layout, and many conveyors move at the same time.',
    },
    {
      n: '04',
      k: 'Vertical where it pays',
      v: 'Stackers above selected conveyors, or above every conveyor, lift cars into simple storage levels: up to four cars on the footprint of one.',
    },
  ],
  patent:
    'The TilePark XY sliding-puzzle principle is protected by European patent EP 3924576 B1, with further patents pending in the US and Germany.',
};

export const economics = {
  eyebrow: 'The economics of change',
  title: 'A floor that moves changes what a building can earn.',
  body: 'Every square metre that is not a ramp or an aisle can hold a car, or can be given back to the building.',
  levers: [
    {
      k: 'Space utilisation',
      v: 'Every position is a conveyor. With no ramps or driving lanes, almost the entire floor area is used for parking.',
    },
    {
      k: 'Developable area',
      v: 'The same number of cars on less floor area can free space for other uses, or reduce how far the building has to go underground.',
    },
    {
      k: 'Freedom from fixed layouts',
      v: 'Without a shuttle aisle or a central lift core, irregular plots, columns and awkward corners are no longer a problem.',
    },
    {
      k: 'Lighter construction',
      v: 'Only the transport level carries conveyors. Storage levels above are simple steel shelving: no intermediate slabs, lower loads, a shallower pit.',
    },
    {
      k: 'Scalable and modular',
      v: 'The grid is built from identical, industry-standard modules, so a system is sized to the site rather than to a machine.',
    },
  ],
  example: {
    title: 'Worked example',
    caption: 'From the TilePark planning model used on this page. Illustrative, not a project result.',
    rows: [
      { config: 'XY only, one level', cars: '19', perCar: '15.6 m²', height: '≈ 2.45 m' },
      { config: 'Stackers above 11 conveyors, 4 levels', cars: '52', perCar: '5.7 m²', height: '9.14 m' },
      { config: 'Stackers above every conveyor, 4 levels', cars: '91', perCar: '3.3 m²', height: '9.14 m' },
    ],
    assumptions: [
      'Grid of 6 × 4 conveyors, 14.0 m × 21.2 m (≈ 297 m²).',
      'Pallet pitch 2.30 m × 5.25 m, plus 0.10 m clearance to the building.',
      '5 of the 24 conveyors are kept free so cars can be moved.',
      'Floor area per car counts the grid only: transfer cabin, access and technical rooms are excluded.',
      'Clear height for one level depends on vehicle height and is approximate.',
    ],
  },
};

export const next = {
  eyebrow: 'Built for what comes next',
  title: 'Infrastructure that keeps up with mobility.',
  body: 'A building outlives several generations of cars. We separate clearly what TilePark does today, what we are developing, and where we are heading.',
  today: [
    {
      k: 'Integrated EV charging',
      v: 'Every pallet can be charge-ready. Once a car reaches the charge set in the app, the system moves it away so the next car can charge.',
    },
    {
      k: 'Software-driven operation',
      v: 'Valet requests, guest access, fleets and payment run in one app, with an operator platform for billing, users and live occupancy.',
    },
    {
      k: 'Remote diagnostics and updates',
      v: 'Like a modern car, TilePark receives remote updates: new functions and improvements without a site visit.',
    },
    {
      k: 'Resilience',
      v: 'Every conveyor has at least four drive motors. With as little as 30 amps, the system can run on a generator during a power outage.',
    },
  ],
  developing: [
    {
      k: 'Learning from operation',
      v: 'Every sequence is a lesson in which routes and storage positions work best. TilePark has begun implementing these learning capabilities, using anonymous usage patterns, never personal tracking.',
    },
  ],
  future: [
    {
      k: 'Autonomous mobility',
      v: 'Cars are handed over in a transfer cabin and moved without anyone inside, a natural interface for vehicles that arrive on their own. A direction of development, not a current feature.',
    },
    {
      k: 'Evolving buildings',
      v: 'Because capabilities arrive as software, a system can keep improving over the building’s life rather than being replaced.',
    },
  ],
};

export const heritage = {
  eyebrow: 'Engineering heritage',
  title: 'We design what we build, and we build what we develop.',
  body: [
    'Parkstory combines generations of mechanical engineering and manufacturing experience with decades of advanced software development.',
    'Our philosophy is that engineering excellence requires mastery of manufacturing. The integration of development, production and process control is fundamental to the quality and reliability we aim to deliver.',
  ],
  facts: [
    {
      k: 'Kehl, Germany',
      v: 'Approximately 10,000 m² of sheet-metal processing, welding and assembly under one roof.',
    },
    { k: 'Gastonia, North Carolina', v: 'Production, machining and assembly for North America.' },
    { k: 'Own controls', v: 'The decentralised control system that runs every conveyor is developed in-house.' },
    { k: '100 % tested', v: 'Every conveyor passes a functional test and is load-tested on a rig before shipping.' },
    { k: 'Serialised', v: 'Every component carries a serial number, and every test result is logged against it.' },
    {
      k: '30+ years',
      v: 'Spare parts guaranteed for at least 30 years, because we own the drawings, tooling and production.',
    },
  ],
  flow: ['Design', 'Controls', 'Steel & cutting', 'Welding', 'Pre-assembly', '100 % test', 'Installation', 'Service'],
};

export const decision = {
  title: 'The most expensive parking system may be the one you cannot adapt.',
  body: 'Before committing to decades of parking infrastructure, compare the architectures. We invite developers, architects, investors and owners to explore TilePark with our engineers, early in the design.',
  cta: 'Request a technology briefing',
  // Placeholder until Parkstory provides a contact address or form.
  ctaHref: '#decision',
  secondary: 'Watch TilePark in operation',
  secondaryHref: 'https://www.youtube.com/@parkstory2332',
  audience: ['Architects', 'Developers', 'Investors', 'Owners & operators'],
};

export const nature = {
  eyebrow: 'Inspired by nature',
  title: 'We asked the bees how to park.',
  body: 'Bees have been solving our problem for millions of years: storing as much as possible in as little space as possible, and getting everywhere fast. Here are their five rules, and how TilePark follows each one.',
  rules: [
    {
      q: 'Don’t waste a single cell.',
      bees: 'A honeycomb stores the most in the least space. No other shape divides an area into equal cells with less wall, a fact proven mathematically in 1999.',
      tp: 'Every position is a conveyor. No ramps, no driving lanes, no wasted floor.',
    },
    {
      q: 'Take the shortest way.',
      bees: 'Bees learn the shortest route between flowers, even when they found them in a different order.',
      tp: 'For every request, the system calculates the fastest route for the grid’s current layout.',
    },
    {
      q: 'Nobody is in charge.',
      bees: 'A hive has no boss and no master plan. Thousands of bees follow simple rules, and order emerges on its own.',
      tp: 'Each conveyor has its own controller and hands cars to its neighbours. No central computer.',
    },
    {
      q: 'If a cell breaks, go around it.',
      bees: 'Bees simply work around a damaged cell. The colony keeps going.',
      tp: 'If a conveyor goes offline, the others route around it, and every car stays accessible.',
    },
    {
      q: 'Keep getting better.',
      bees: 'Bees refine their route with every flight and keep whatever is shorter.',
      tp: 'Every sequence teaches the system which routes and positions work best.',
    },
  ],
};

export const ev = {
  eyebrow: 'Integrated EV charging',
  title: 'Every space can charge.',
  titleAccent: 'Every charger keeps working.',
  body: 'With fixed charging bays, a fully charged car blocks the charger until its driver returns. TilePark moves each EV to a charger, charges it to the level requested in the app, and then moves it away so the next vehicle can charge. Chargers never sit idle.',
  features: [
    {
      k: 'Every pallet is EV-ready',
      v: 'No dedicated charging bays and no wasted spaces. Park on the pallet, plug in your own cable at the Level 2 socket, and start charging from the app.',
    },
    {
      k: 'Fewer chargers, higher utilisation',
      v: 'Because chargers never sit blocked, a small number of charging points can serve every EV in the garage. Fewer chargers to buy, more revenue per charger.',
    },
    {
      k: 'Metered and billed in the app',
      v: 'Live kWh, stop at any time, and pay in the same app that manages your arrival and pickup. Automated re-parking means no idle fees.',
    },
    {
      k: 'Smart load management',
      v: 'Charging power is managed intelligently across the whole system, and capacity can grow with demand without rebuilding the garage.',
    },
  ],
  driver: [
    'No waiting for a free charging station',
    'Automated re-parking after charging, so no idle fees',
    'One seamless journey, from arrival to pickup, in one app',
  ],
  owner: [
    'Fewer dedicated charging points needed',
    'Expandable as demand grows',
    'Intelligent load management across the whole system',
  ],
};

/**
 * Why TilePark is the disruptor: system design, decentralised intelligence,
 * simple mechanics and fast reaction through in-house R&D. Every statement is
 * taken from Parkstory's existing material; no comparison with named
 * competitors and no superlatives that cannot be shown.
 */
export const edge = {
  eyebrow: 'Why TilePark leads',
  title: 'Intelligent where it matters.',
  titleAccent: 'Simple where it counts.',
  body: 'What makes TilePark disruptive is not a single feature. It is how the system is designed, and how Parkstory develops it.',
  pillars: [
    {
      n: '01',
      k: 'Designed differently',
      v: 'The floor itself is the machine. Instead of a few central shuttles, lifts or cranes that every car must pass through, every position is a conveyor that moves a car lengthwise and crosswise.',
    },
    {
      n: '02',
      k: 'Decentralised intelligence',
      v: 'Each conveyor has its own controller and acts independently. Routes are calculated for the grid’s current layout, many conveyors move at the same time, and a single fault never stops the garage.',
    },
    {
      n: '03',
      k: 'Simple, reliable mechanics',
      v: 'Because the intelligence lives in software, the steel can stay simple: identical, pre-assembled modules built from industry-standard components, robust and easy to service.',
    },
    {
      n: '04',
      k: 'Fast to react',
      v: 'Mechanics, controls, software and the app are developed by our own team and built in our own factories. Improvements reach the field as remote updates, and remote diagnostics let our team respond to any issue immediately.',
    },
  ],
  software: [
    'Decentralised control: a controller in every conveyor',
    'Routes calculated for the current layout',
    'Many conveyors moving in parallel',
    'Learning from operation (in development)',
    'Remote diagnostics and remote updates',
  ],
  mechanics: [
    'Identical conveyor modules, pre-assembled and 100 % tested',
    'Industry-standard components',
    'At least four drive motors per conveyor; any conveyor can take over for any other',
    'Cars only move horizontally on the transport level',
    'Storage levels are simple steel shelving',
  ],
  loop: ['Engineering', 'Controls & software', 'Own factories', 'In operation', 'Remote updates'],
  loopNote:
    'One company from first sketch to service: no importer, no third-party system and no outside assembler between an idea and the garage that runs it.',
};

/** The app as the user-facing end of decentralised control. */
export const app = {
  eyebrow: 'The TilePark app',
  title: 'Decentralised control,',
  titleAccent: 'in the driver’s hand.',
  body: 'TilePark has no central master that every car depends on. The app takes that principle all the way to the people who use the garage: it puts each driver in charge of their own car, their own guests and their own schedule. It is the one part of TilePark that puts you at the center.',
  features: [
    {
      t: 0,
      k: 'Your valet, on call',
      v: 'Announce your departure, or schedule it in advance, and your car is waiting in the transfer cabin when you arrive. No queue, no keys to hand over.',
    },
    {
      t: 5,
      k: 'Manage your cars',
      v: 'Several vehicles and users in one account. Enter with a QR code, a secure access code or license-plate recognition.',
    },
    {
      t: 2,
      k: 'Welcome your guests',
      v: 'Grant friends, family and visitors access with a tap, for one evening or for good, and revoke it at any time.',
    },
    {
      t: 1,
      k: 'Plan and charge',
      v: 'Set your next departure and your charge target. Once charging is complete, the system moves the car away and frees the charger.',
    },
    {
      t: 3,
      k: 'Fleets, company and hotel parking',
      v: 'An operator platform with user management, live dashboards and dynamic pricing for company vehicles, employees and hotel guests.',
    },
    {
      t: 4,
      k: 'Payment',
      v: 'Parking, charging and guest access paid in the app, for subscribers and occasional users alike, with every receipt in one place.',
    },
  ],
  operators: [
    { k: 'Billing', v: 'Subscriptions, short-term parking, EV charging and guest access, billed automatically.' },
    { k: 'User management', v: 'Add, change and remove users, vehicles and access rights in a few clicks.' },
    {
      k: 'Groups and roles',
      v: 'Residents, employees, hotel guests or pool cars, each with their own rules, rates and time windows.',
    },
    {
      k: 'Live dashboard',
      v: 'Occupancy, charging, revenue and system status at a glance, with reports for every period.',
    },
  ],
};

/** Quality control on the load test rig (with the load-test video). */
export const quality = {
  eyebrow: 'Quality control',
  title: 'Every conveyor segment is',
  titleAccent: 'tested under load.',
  body: 'Before a conveyor leaves our factory, it goes onto the test rig. A hydraulic press applies load from above while the drives run, just as they will under a parked car. Only conveyors that pass are released for shipping.',
  checks: [
    { k: 'Drives, gearboxes and rollers', v: 'run under load, not just switched on.' },
    { k: 'Structure and alignment', v: 'are checked while the conveyor carries weight.' },
    { k: 'Every result is logged', v: 'against the component’s serial number.' },
  ],
  caption: 'Conveyor segment on the load test rig',
};
