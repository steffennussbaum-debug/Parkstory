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
  title: 'Your vision needs space. We unlock it.',
  lead: 'Every square foot consumed by an inefficient parking solution is a square foot your development can never recover.',
  intro: 'Residents need parking, but every square foot it occupies is space you can’t market.',
  points: [
    { n: '01', text: 'Automated parking is undergoing a technological transformation.' },
    { n: '02', text: 'TilePark is a new architecture, designed for the cities and buildings of tomorrow.' },
    { n: '03', text: 'The system you choose today will shape the building for decades.' },
  ],
};

export const question = {
  eyebrow: 'The question',
  title: 'Have you chosen the right parking system supplier for the decades ahead?',
  body: 'An automated parking system is not bought for opening day. For decades, the building will depend on its architecture, its controls, its spare parts and the company behind it. Before you sign, these are the questions worth asking every supplier, including us.',
  constraints: [
    {
      k: 'Does every car depend on a single machine?',
      v: 'If one shuttle, lift or crane stops, every car behind it waits. Ask whether the system can route around a fault and keep every car accessible.',
    },
    {
      k: 'Will the system improve after opening day?',
      v: 'Years pass between the decision and the first car. Ask whether new capabilities arrive as software updates, or whether the system stays as it was specified.',
    },
    {
      k: 'Who designs and builds the technology?',
      v: 'Mechanics, controls, software and app from one company, or integrated from third parties? The answer decides who can fix, improve and support the system.',
    },
    {
      k: 'Will parts and support still exist in decades?',
      v: 'Ask how long spare parts are guaranteed, and whether that guarantee depends on other companies’ catalogues.',
    },
    {
      k: 'Does the system adapt to the building?',
      v: 'Irregular plots, columns, EV charging, additional levels: ask whether the layout adapts to the site, or the site to the machine.',
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
      v: 'The floor is a grid of conveyors, each able to move a car in both X and Y directions. Each car rests on its own pallet and moves like a tile in a sliding puzzle.',
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
  body: 'A building outlives several generations of cars. We separate clearly what TilePark does today, what we keep developing, and where we are heading.',
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
      k: 'Swarm technology through AI',
      v: 'Like a swarm, every TilePark learns, and all systems learn from each other. Each sequence teaches which routes and storage positions work best, and every garage contributes to this shared intelligence through anonymous usage patterns, such as typical arrival and departure times, never through personal tracking. Parkstory has begun implementing these learning capabilities and keeps extending them.',
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
    'Swarm learning through AI: all systems learn from each other (continuous development)',
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

/* ------------------------------------------------------------------------
 * Additional explainer content from Parkstory's "How TilePark works" page,
 * used by Concept B to restore the depth and flow of the original.
 * --------------------------------------------------------------------- */

/** From arrival to pickup. */
export const journey = [
  {
    k: 'Effortless drop-off',
    v: 'Drive into the friendly and safe transfer cabin, switch off the engine, and step out. From that moment on, the system takes over, and no one ever has to walk through the garage.',
  },
  {
    k: 'Fully automated parking',
    v: 'Your car stays on its own pallet throughout. The conveyors beneath move it precisely in X and Y to an available position, without anyone at the wheel.',
  },
  {
    k: 'Secure, space-efficient storage',
    v: 'Without ramps, driving lanes, or walkways, almost the entire floor area is available for parking. The storage area is not accessible to the public.',
  },
  {
    k: 'Ready when you are',
    v: 'Request your car via app or terminal. The system calculates the best route, moves the surrounding cars aside, and presents your car in the transfer cabin.',
  },
];

/** Who benefits from the architecture. */
export const audience = [
  {
    who: 'For architects',
    k: 'The grid adapts to the site',
    v: 'Without a fixed shuttle aisle or a central lift core dictating the layout, irregular plots, columns, and awkward corners all become usable parking.',
  },
  {
    who: 'For developers',
    k: 'No single point of failure',
    v: 'A faulty conveyor never shuts down the garage. That protects uptime, tenant satisfaction, and the long-term value of the asset.',
  },
  {
    who: 'For everyone',
    k: 'Conveyors everywhere, no aisles',
    v: 'Every position is a conveyor. With no ramps or driving lanes, almost the entire floor area is used for parking.',
  },
];

/** The third dimension: stackers. */
export const third = {
  eyebrow: 'The third dimension',
  title: 'Add Z.',
  titleAccent: 'Up to four cars on the footprint of one.',
  body: 'The XY grid moves cars across the floor. Add a TilePark stacker above selected conveyors, or above every conveyor, and the footprint of a single car holds up to four cars instead of one.',
  steps: [
    {
      k: 'XY handles the logistics',
      v: 'The transport level brings each car beneath its stacker, using the same sliding-puzzle routing.',
    },
    {
      k: 'The stacker lifts it up',
      v: 'The stacker raises the car into a storage level directly above its conveyor. The storage levels need no conveyors, because cars are stacked as in a silo.',
    },
    {
      k: 'And brings it back down',
      v: 'On request, the stacker lowers the car onto a free conveyor, which carries it to the transfer cabin.',
    },
    {
      k: 'Still no single point of failure',
      v: 'Each stacker serves only its own conveyor. With no central lift tower that every car depends on, the rest of the garage keeps running.',
    },
  ],
  whyTitle: 'One automation level.',
  whyAccent: 'Everything above is simple storage.',
  whyBody:
    'All of the automation is concentrated on the transport level. The levels above are stacked like a silo and need neither conveyors nor floor slabs. The building becomes simpler, lighter, and less expensive.',
  why: [
    {
      k: 'Conveyors on one level only',
      v: 'Conveyors and drives are installed on the transport level alone. The storage levels are simple steel shelving: less equipment to purchase and maintain.',
    },
    {
      k: 'No slabs to build',
      v: 'A stacked silo replaces intermediate parking decks, eliminating concrete slabs, formwork, and reinforcement.',
    },
    {
      k: 'No height lost to slabs',
      v: 'Without slabs and their build-up, every meter of height is used for cars, so more levels fit within the same building.',
    },
    {
      k: 'Lower build-up height',
      v: 'The XY conveyor level itself is very low, which saves floor height, pit depth and construction cost.',
    },
    {
      k: 'Lightweight construction',
      v: 'The light steel structure means lower loads on the building, smaller foundations, and an easy fit in existing structures.',
    },
    {
      k: 'Less excavation',
      v: 'A lower structure for the same number of cars means a shallower pit, reducing excavation, shoring, and waterproofing.',
    },
  ],
  whyFoot:
    'It unlocks height. Whether in a basement, on a ground floor, or in a dedicated building, the clear height you already have becomes parking capacity.',
};

/** Resilience during a power outage. */
export const power = {
  title: 'And if the power goes out?',
  titleAccent: 'Your car still comes out.',
  body: 'TilePark requires remarkably little power. With as little as 30 amps, the entire system can run on a generator, so drivers can still collect their cars during a power outage.',
  points: [
    {
      k: 'Low energy use.',
      v: 'On the XY level, cars only ever move horizontally, along the shortest optimized routes. Only the conveyors needed for a sequence move.',
    },
    {
      k: 'Multiple redundancy.',
      v: 'Every conveyor has at least four drive motors, and every conveyor can take over for any other.',
    },
    { k: 'No single point of failure.', v: 'If one conveyor is down, the others route around it.' },
  ],
};

/** Designed around the driver. */
export const driver = {
  eyebrow: 'Designed around the driver',
  title: 'Behind the machine,',
  titleAccent: 'it is all about you.',
  items: [
    {
      k: 'Your time, not the system’s',
      v: 'Retrieval is planned around your schedule. Tell the app when you leave, or let it learn your routine, and your car is waiting instead of you.',
    },
    {
      k: 'No searching, no guessing',
      v: 'No ramps, no levels, no hunting for a free space or for where you parked. You always know where your car is and when it will be ready.',
    },
    {
      k: 'Safe and stress-free',
      v: 'No dark stairwells, no tight ramps and no walking through a garage at night. You only ever enter the friendly and safe transfer cabin.',
    },
    {
      k: 'Your circle, your rules',
      v: 'Family, guests, a valet or a colleague: you decide who may use the garage, when, and with which car, and you can change it at any time.',
    },
    {
      k: 'Always informed',
      v: 'Notifications tell you when your car is ready, when charging is complete and when a booking is about to end.',
    },
    {
      k: 'One app, one journey',
      v: 'Access, parking, charging, guests and payment in one place, with no tickets, no cards and no second app.',
    },
  ],
};

/**
 * Owning the entire value chain. The contrast with the market is stated in
 * general terms as Parkstory's own market assessment; no supplier is named.
 */
export const valueChain = {
  eyebrow: 'One company, the entire value chain',
  title: 'You can’t control what you don’t',
  titleAccent: 'design and build yourself.',
  body: 'In automated parking, the value chain is often split between several companies: one designs the system, others manufacture it, supply the controls or write the software. Parkstory owns all of it. Our engineers design every TilePark system, our team writes the controls and the app, and our own factories in Kehl, Germany, and Gastonia, USA, build it from raw steel to finished conveyor.',
  steps: [
    { k: 'Engineering', v: 'Mechanical, electrical and structural' },
    { k: 'Controls', v: 'Decentralised, developed in-house' },
    { k: 'Software & app', v: 'App and operator platform' },
    { k: 'Steel processing', v: 'Laser cutting and CNC bending' },
    { k: 'Welding', v: 'Robotic and manual' },
    { k: 'Machining', v: 'CNC turning and machining' },
    { k: 'Assembly', v: 'Drives and pre-assembly' },
    { k: 'Testing', v: '100 %, under load' },
    { k: 'Installation', v: 'By our own team' },
    { k: 'Service', v: 'Remote updates, 30+ years of parts' },
  ],
  statement: 'Every step. One company. One team that knows your system.',
  pillars: [
    { k: 'Designed in-house', v: 'Every component is designed specifically for TilePark by our own engineers.' },
    { k: 'Our own controls', v: 'The decentralised control system is developed in-house. We know every line of code.' },
    {
      k: 'Made in our own factories',
      v: 'Laser cutting, bending, robotic welding and assembly under our own roof, in Germany and the USA.',
    },
    {
      k: 'Pre-assembled, 100 % tested',
      v: 'Every system is pre-assembled at the plant; every conveyor passes a full functional test.',
    },
    {
      k: 'Spare parts for 30+ years',
      v: 'Because we own the drawings, the tooling and the production, independent of any supplier’s catalogue.',
    },
    {
      k: 'One partner, start to finish',
      v: 'Design, production, installation and service from one company under one contract.',
    },
    {
      k: 'Every component serialised',
      v: 'Each component can be traced at any time, so we keep full control of quality and supply chain.',
    },
    {
      k: 'Industry-standard parts',
      v: 'Proven industrial parts inside our own design: robust, widely available and easy to service.',
    },
  ],
  banner: {
    title: 'Built in our factories. Installed in your building.',
    caption: 'TilePark conveyors with their drives, pre-assembled and tested before delivery.',
  },
  plants: [
    {
      flag: 'DE',
      name: 'Kehl, Germany',
      text: 'Parkstory Manufacturing Kehl: approximately 10,000 m² of sheet-metal processing, welding and assembly under one roof.',
      caps: [
        'Coil processing and laser cutting',
        'CNC bending up to 6 m',
        'Robotic and manual welding',
        'CNC turning',
        'Steel structures and assembly',
        'Pre-assembly and functional testing',
      ],
    },
    {
      flag: 'US',
      name: 'Gastonia, North Carolina, USA',
      text: 'Production, machining and assembly for North America: TilePark, built in the USA.',
      caps: [
        'Fiber laser cutting with automatic shuttle table',
        'CNC press brake bending',
        'CNC turning and machining centers',
        'Welding and steel fabrication',
        'Conveyor drive assembly and testing',
        'Gantry and jib cranes for heavy assemblies',
      ],
    },
  ],
  youtube: 'https://www.youtube.com/@parkstory2332',
};

/**
 * Innovation and engineering. Statements are Parkstory's own; the
 * automation strategy summarises principles already shown on the page
 * (one automation level, decentralised control, software-first, learning).
 */
export const innovation = {
  eyebrow: 'Engineering and innovation',
  title: 'Innovation is',
  titleAccent: 'our DNA.',
  body: 'TilePark was not adapted from an existing parking machine. It was engineered from first principles by one team that covers every discipline the system needs, and it keeps evolving in our own hands.',
  disciplines: [
    {
      k: 'Mechanical engineering',
      v: 'Conveyors, drives, stackers and steel structures, designed specifically for TilePark.',
    },
    { k: 'Electrical engineering', v: 'Drives, power distribution and charging integration, down to every conveyor.' },
    { k: 'Structural engineering', v: 'Steel structures and integration into new and existing buildings.' },
    { k: 'Controls', v: 'The decentralised control system that runs every conveyor. We know every line of code.' },
    {
      k: 'Software and AI',
      v: 'Route planning, swarm learning, remote diagnostics and updates, developed with AI-backed software engineering.',
    },
    {
      k: 'App and platform',
      v: 'The driver app and the operator platform: valet, guests, fleets, charging and payment.',
    },
  ],
  aiTitle: 'AI-backed software engineering',
  aiBody:
    'Software is where TilePark’s intelligence lives, so it is where we invest. Our team uses AI throughout software engineering, and builds AI into the product itself: every TilePark learns which routes and storage positions work best, and all systems learn from each other.',
  strategyTitle: 'A clear automation strategy, at the core of the product',
  strategy: [
    {
      n: '01',
      k: 'Automate where it creates value',
      v: 'Only the transport level is automated. Everything above is simple steel storage.',
    },
    {
      n: '02',
      k: 'Decentralise everything',
      v: 'A controller in every conveyor. No master computer, no single machine every car depends on.',
    },
    {
      n: '03',
      k: 'Software first',
      v: 'New capabilities arrive as remote updates, so a system keeps improving for decades.',
    },
    { n: '04', k: 'Learn continuously', v: 'Swarm learning through AI: every sequence makes every system better.' },
  ],
  patent: 'Patented principle: European patent EP 3924576 B1, with further patents pending in the US and Germany.',
};

/**
 * Project delivery and after-sales service. The uptime benchmark and the
 * service figures (24/7, 99 % solved remotely) are Parkstory's own
 * statements and must match its service contracts.
 */
export const delivery = {
  eyebrow: 'From first sketch to decades of operation',
  title: 'One partner leads',
  titleAccent: 'every phase.',
  body: 'Parkstory leads and manages the entire process itself: planning, engineering, manufacturing, commissioning and after-sales service. One company, one contract, one team that knows your system from the first sketch.',
  phases: [
    {
      k: 'Planning',
      v: 'Together with architects and developers from the first sketch: the grid, stackers, transfer cabins and EV charging fitted to the site and the building.',
    },
    {
      k: 'Engineering',
      v: 'Our engineers design the mechanical, electrical and structural system and configure the controls for your project.',
    },
    {
      k: 'Manufacturing',
      v: 'Built and pre-assembled in our own factories in Kehl and Gastonia. Every conveyor is load-tested before shipping.',
    },
    {
      k: 'Commissioning',
      v: 'Installed and commissioned by our own team, and handed over by the people who built it.',
    },
    {
      k: 'After-sales service',
      v: '24/7 availability, remote diagnostics and updates, and spare parts for at least 30 years.',
    },
  ],
  uptime: {
    value: '99.5 %',
    label: 'uptime',
    claim: 'A system that doesn’t deliver 99.5 % uptime has failed.',
    note: 'That is the standard we hold TilePark to, and why every phase stays in our hands.',
  },
  service: {
    title: 'After-sales service, around the clock',
    steps: [
      { k: '24/7', v: 'Our after-sales team is available around the clock, every day of the year.' },
      {
        k: 'Kiosk or app',
        v: 'Drivers and operators reach us directly from the kiosk or the app, in their own language.',
      },
      {
        k: '99 % solved remotely',
        v: 'Our after-sales team solves 99 % of all issues remotely, through remote diagnostics.',
      },
      { k: 'On site', v: 'If an issue cannot be solved remotely, a Parkstory technician comes on site.' },
    ],
  },
};
