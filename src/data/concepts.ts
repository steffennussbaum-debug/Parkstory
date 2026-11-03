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
