import { getPermalink } from './utils/permalinks';

// Header and footer links for the Parkstory site. The home page sections are
// linked by their anchors (#how-it-works, …).
export const headerData = {
  links: [
    {
      text: 'Technology',
      links: [
        { text: 'Inspired by nature', href: getPermalink('/#inspired-by-nature') },
        { text: 'How it works', href: getPermalink('/#how-it-works') },
        { text: 'The third dimension', href: getPermalink('/#third-dimension') },
        { text: 'The heart of TilePark', href: getPermalink('/#heart') },
      ],
    },
    { text: 'EV charging', href: getPermalink('/#ev-charging') },
    { text: 'The app', href: getPermalink('/#app') },
    {
      text: 'Company',
      links: [
        { text: 'Future-proof', href: getPermalink('/#future-proof') },
        { text: 'Made by Parkstory', href: getPermalink('/#factories') },
        { text: 'Quality control', href: getPermalink('/#quality') },
      ],
    },
  ],
  actions: [{ text: 'See it in action', href: 'https://www.youtube.com/@parkstory2332', target: '_blank' }],
};

export const footerData = {
  links: [
    {
      title: 'Technology',
      links: [
        { text: 'Inspired by nature', href: getPermalink('/#inspired-by-nature') },
        { text: 'How it works', href: getPermalink('/#how-it-works') },
        { text: 'The third dimension', href: getPermalink('/#third-dimension') },
        { text: 'The heart of TilePark', href: getPermalink('/#heart') },
      ],
    },
    {
      title: 'For you',
      links: [
        { text: 'EV charging', href: getPermalink('/#ev-charging') },
        { text: 'The app', href: getPermalink('/#app') },
        { text: 'Future-proof', href: getPermalink('/#future-proof') },
      ],
    },
    {
      title: 'Company',
      links: [
        { text: 'Made by Parkstory', href: getPermalink('/#factories') },
        { text: 'Quality control', href: getPermalink('/#quality') },
        { text: 'YouTube', href: 'https://www.youtube.com/@parkstory2332' },
      ],
    },
  ],
  secondaryLinks: [],
  socialLinks: [{ ariaLabel: 'YouTube', icon: 'tabler:brand-youtube', href: 'https://www.youtube.com/@parkstory2332' }],
  footNote: `
    Designed, programmed and built by Parkstory in Kehl, Germany, and Gastonia, USA.
  `,
};
